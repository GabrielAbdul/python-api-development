'''module defines all pydantic schemas'''

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, conint


class UserBase(BaseModel):
    '''validate User input'''
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    '''defines user operation responses'''
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        # converts sqlalchemy model into pydantic object for dict conversion
        orm_mode = True


class PostBase(BaseModel):
    '''validate Post Input'''
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    '''defines post GET input'''
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    likes: int

class Like(BaseModel):
    '''defines payload of vote from user'''
    post_id: int
    dir: conint(le=1)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
