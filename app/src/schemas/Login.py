# 3rd party imports
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class Scopes(str, Enum):
    BASIC = "basic"
    ADMIN = "admin"
    OTP_CHECKED = "otp_checked"


class LoginForm(BaseModel):
    username: str = Field(..., min_length=2, max_length=32)
    password: str = Field(..., min_length=8, max_length=64)
    model_config = {"extra": "forbid"}


class RegisterForm(LoginForm):
    password_rep: str = Field(..., min_length=8, max_length=64)
    email: EmailStr
    model_config = {"extra": "forbid"}


class User(BaseModel):
    username: str = Field(..., min_length=2, max_length=32)
    email: EmailStr
    is_disabled: Optional[bool] = False
    is_admin: Optional[bool] = False
    
    otp_enabled: bool = False
    otp_verified: bool = False
    
    class Config:
        from_attributes = True


class UserDB(User):
    password_hash: str = Field(..., max_length=256)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    otp_base32: str | None = None
    otp_auth_url: str | None = None
    
    class Config:
        from_attributes = True


class UserRequestSchema(BaseModel):
    token: str = Field(..., min_length=6, max_length=6)


class ForgotPasswordForm(BaseModel):
    account: str|EmailStr
    model_config = {"extra": "forbid"}


class ResetPasswordForm(BaseModel):
    password: str = Field(..., min_length=8, max_length=64)
    password_rep: str = Field(..., min_length=8, max_length=64)
    model_config = {"extra": "forbid"}