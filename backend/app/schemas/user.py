from pydantic import BaseModel, EmailStr
from enum import Enum

class Role(str, Enum):
    ADMIN = "ADMIN"
    MAINTAINER = "MAINTAINER"
    REPORTER = "REPORTER"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str
    role: Role = Role.REPORTER

class UserOut(UserBase):
    id: int
    role: Role

    class Config:
        from_attributes = True  # updated for Pydantic v2 (replaces orm_mode)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int
    role: Role

# Alias User to UserOut for backward compatibility (so you can do `from app.schemas.user import User`)
User = UserOut
