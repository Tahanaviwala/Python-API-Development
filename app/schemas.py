from datetime import datetime
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(Post):
    pass

class PostResponse(Post):
    id: int
    created_at: datetime
    
    class Config():
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
    
    class Config():
        orm_mode = True
