# 3rd party imports
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class LoginForm(BaseModel):
    username: str = Field(..., min_length=2, max_length=32)
    password: str = Field(..., min_length=8, max_length=64)
    model_config = {"extra": "forbid"}


class RegisterForm(LoginForm):
    email: EmailStr
    discord: Optional[str] = Field(None, min_length=3, max_length=32)
    model_config = {"extra": "forbid"}


class User(BaseModel):
    username: str = Field(..., min_length=2, max_length=32)
    email: EmailStr
    discord: Optional[str] = Field(None, min_length=3, max_length=32)
    disabled: Optional[bool] = False
    is_admin: Optional[bool] = False
    
    class Config:
        from_attributes = True


class UserDB(User):
    password_hash: str = Field(..., max_length=256)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    otp_enabled: bool = False
    otp_verified: bool = False

    otp_base32: str | None = None
    otp_auth_url: str | None = None
    
    class Config:
        from_attributes = True


class UserRequestSchema(BaseModel):
    username: str = Field(..., min_length=2, max_length=32)
    token: str | None = None

