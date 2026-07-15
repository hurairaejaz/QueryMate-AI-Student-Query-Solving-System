from dataclasses import Field

from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime


class AdminRegisterIn(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class AdminLoginIn(BaseModel):
    email: EmailStr
    password: str


class MeOut(BaseModel):
    user_id: int
    email: str
    role: str
    full_name: Optional[str] = None

    class Config:
        from_attributes = True


class ForgotPasswordRequest(BaseModel):
    identifier: str  # email or phone


class ForgotPasswordResponse(BaseModel):
    message: str


class ResetPasswordRequest(BaseModel):
    identifier: str
    otp_code: str
    new_password: str


class ResetPasswordResponse(BaseModel):
    message: str

class ForgotPasswordIn(BaseModel):
    identifier: str

class VerifyOtpIn(BaseModel):
    identifier: str
    otp_code: str

class ResetPasswordIn(BaseModel):
    identifier: str
    otp_code: str
    new_password: str

class MessageOut(BaseModel):
    message: str

# user sighnup

class UserRegister(BaseModel):
     full_name: str
     phone: str
     email: EmailStr
     password: str
     roll_number: Optional[str] = None

class UserOut(BaseModel):
    user_id: int
    full_name: str
    phone: str | None = None
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True
        
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut
    
class RegisterResponse(BaseModel):
    message: str
    access_token: str | None = None
    token_type: str | None = "bearer"
    user: UserOut
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# class ForgotPasswordIn(BaseModel):
#     phone: str


# class VerifyOtpIn(BaseModel):
#     phone: str
#     otp: str


# class ResetPasswordIn(BaseModel):
#     phone: str
#     otp: str
#     new_password: str