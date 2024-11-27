from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# User Base Model Schema
class UserBase(BaseModel):
    email: EmailStr
    username: str

# User Create Schema
class UserCreate(UserBase):
    password: str

# User Schema used also for response
class User(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User Schema for Token Data
class TokenData(BaseModel):
    user_id: Optional[int] = None

# User Schema for Token
class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str

class EmailVerify(BaseModel):
    email: EmailStr

class CodeVerify(BaseModel):
    email: EmailStr
    code: int

class PasswordReset(BaseModel):
    email: EmailStr
    new_password: str