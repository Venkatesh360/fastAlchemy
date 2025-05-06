from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import user_schema
from ..models import user_model
from .. import database
from ..utils import utils

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=user_schema.UserResponse)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    # Hash the password and create a new user
    hashed_password = utils.hash_password(user.password)
    new_user = user_model.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/signin", response_model=user_schema.SigninResponse)
def signin(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    # Authenticate user
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password): #type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate access token
    token = utils.create_access_token({"sub": db_user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": db_user
    }
