from pydantic import BaseModel, EmailStr
from  datetime import datetime


class UserCreate(BaseModel):
    """
    Pydantic model for user registration data.

    Attributes:
        username (str): The username chosen by the user.
        email (str): The user's email address.
        password (str): The user's plain-text password.

    This model is used to validate the data when a new user signs up.
    """
    username: str
    email: str
    password: str
    

class UserLogin(BaseModel):
    """
    Pydantic model for user login credentials.

    Attributes:
        email (EmailStr): The user's email address, validated as an email format.
        password (str): The user's plain-text password.

    This model is used to validate login attempts.
    """
    email: EmailStr
    password: str
    
    
class UserResponse(BaseModel):
    """
    Pydantic model for returning user data in the response.

    Attributes:
        username (str): The user's username.
        email (str): The user's email address.
        created_at (datetime): Timestamp of when the user account was created.
        updated_at (datetime): Timestamp of the last update to the user account.

    Config:
        orm_mode (bool): Enables compatibility with ORM models, allowing them to be serialized to Pydantic models.
    """
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
        
class SigninResponse(BaseModel):
    """
    Pydantic model for the response after a successful login.

    Attributes:
        access_token (str): The JWT access token issued to the user.
        token_type (str): The type of token, typically "bearer".
        user (UserResponse): The user data returned as part of the signin process.

    This model is used to return the token and user info after a successful login.
    """
    access_token: str
    token_type: str
    user: UserResponse
    