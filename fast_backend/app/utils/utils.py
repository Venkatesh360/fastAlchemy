import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = str(os.getenv('ALGORITHM'))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/signin")


def hash_password(password: str):
    """
    Hash a plain-text password using bcrypt.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Verify if a plain-text password matches a hashed password.

    Args:
        plain_password (str): The plain-text password to check.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """
    Create a JWT access token with a specified expiration time.

    Args:
        data (dict): The data to encode in the token. Should include a unique user identifier ("sub").
        expires_delta (timedelta, optional): The expiration time of the token. Defaults to 1 hour.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta  
    to_encode.update({
        "exp": expire,
        "sub": str(data.get("sub"))  
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str = Depends(oauth2_scheme)):
    """
    Decode a JWT token and extract the user ID from the "sub" field.

    Args:
        token (str): The JWT token sent by the client.

    Returns:
        str: The user ID (subject) extracted from the token.

    Raises:
        HTTPException: If the token is invalid or missing.
    """
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
