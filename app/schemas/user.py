from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Used for registering new users
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Used for logging in
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Used for returning user data in responses
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True  # Allows returning SQLAlchemy objects directly
