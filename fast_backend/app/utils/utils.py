import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

# Secret & algorithm for JWT
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = str(os.getenv('ALGORITHM'))

# FIXED typo: changed 'oauth2_schene' to 'oauth2_scheme'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/signin")

# Hash a password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify a password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Create an access token with expiration
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta  # Use provided expiration
    to_encode.update({
        "exp": expire,
        "sub": str(data.get("sub"))  # Ensure 'sub' is a string and safe access
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decode and validate token
def decode_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
