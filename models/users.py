import re
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from datetime import datetime, timezone
from typing import Optional


class UserBase(SQLModel):
    """
    User registration response model
    """
    email: EmailStr = Field(default=None, index=True, unique=True)
    full_name: str = Field(nullable=False, max_length=28)


class UserPass(UserBase):
    """
        User base model with password
    """
    password: str

    @field_validator('password')
    def password_check(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserCreate(UserPass):
    """
    User registration request model
    """
    confirm_password: str


class User(UserPass, table=True):
    """
    DB User save model
    """
    user_id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserLogin(SQLModel):
    """
    Pydantic model for User Authentication
    """
    email: EmailStr
    password: str
