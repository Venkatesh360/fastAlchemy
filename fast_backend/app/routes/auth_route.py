from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import user_schema
from ..models import user_model
from .. import database
from ..utils import utils

router = APIRouter()


def get_db():
    """
    Dependency to retrieve a SQLAlchemy database session.

    Yields:
        Session: An active SQLAlchemy session.
    
    Ensures the session is properly closed after the request is completed.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", response_model=user_schema.SigninResponse)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    """
    Sign up a new user and create an access token.

    Args:
        user (UserCreate): The details of the user to be created, including username, email, and password.
        db (Session): SQLAlchemy session for interacting with the database.

    Returns:
        dict: A dictionary containing the `access_token`, `token_type`, and the `user` object.

    Raises:
        HTTPException: If the email is already registered, a 400 status code with a relevant error message is raised.
    """
    existing_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    
    hashed_password = utils.hash_password(user.password)
    new_user = user_model.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = utils.create_access_token({"sub": new_user.id})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": new_user
    }


@router.post("/signin", response_model=user_schema.SigninResponse)
def signin(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    """
    Sign in a user and return an access token.

    Args:
        user (UserLogin): The login credentials of the user, including email and password.
        db (Session): SQLAlchemy session for interacting with the database.

    Returns:
        dict: A dictionary containing the `access_token`, `token_type`, and the authenticated `user` object.

    Raises:
        HTTPException: If the email is not found or the password is incorrect, a 401 status code with an error message is raised.
    """
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password): #type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    
    token = utils.create_access_token({"sub": db_user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": db_user
    }
