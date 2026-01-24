from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(BaseModel):
    id: int
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime

    class Config:
        orm_mode = True

