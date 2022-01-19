from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

from app.database import Base

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str
    client_id: str
    client_secret: str
    user_agent: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class ReplyCreate(BaseModel):
    positive_replies: str
    negative_replies: str
    neutral_replies: str

class ReplyOut(BaseModel):
    id: int
    positive_replies: str
    negative_replies: str
    neutral_replies: str    
    created_at: datetime
    class Config:
        orm_mode = True