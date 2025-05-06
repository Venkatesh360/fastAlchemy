from pydantic import BaseModel, EmailStr
from  datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class UserResponse(BaseModel):
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
        
class SigninResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
    