from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Prompt(BaseModel):
    prompt: str


class SuggestIN(BaseModel):
    prompt: str
    html: str


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    name: str


class User(UserBase):
    id: int
    name: str
    created_at: datetime


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    role: Optional[str] = None



class UserOut(User):
    components: Optional[list] = []
    likes: Optional[list] = []
    comments: Optional[list] = []
    

class ComponentBase(BaseModel):
    description: str
    html: str


class Component(ComponentBase):
    id: int
    created_at: datetime
    user_id: int




class ComponentOut(Component):
    user: UserOut
    likes: Optional[list] = []
    comments: Optional[list] = []


class CommentBase(BaseModel):
    comment: str


class Comment(CommentBase):
    id: int
    created_at: datetime
    user_id: int
    component_id: int



class CommentOut(Comment):
    user: UserOut



class LikeBase(BaseModel):
    pass


class Like(LikeBase):
    id: int
    created_at: datetime
    user_id: int
    component_id: int

class LikeOut(Like):
    user: UserOut
    component: ComponentOut


class LayoutBase(BaseModel):
    name: str
    description: str
    html: str



class Layout(LayoutBase):
    id: int
    created_at: datetime



class LayoutOut(Layout):
    user: UserOut



class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None



