import bson
from pydantic import BaseModel, EmailStr, SecretStr, field_validator
from utils.validation import validate_password_strength, validate_username_format, validate_otp_format

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        return validate_username_format(v)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        password = v.get_secret_value()
        validate_password_strength(password)
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr

class ChangePassword(BaseModel):
    current_password: SecretStr
    new_password: SecretStr
    confirm_password: SecretStr
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        password = v.get_secret_value()
        validate_password_strength(password)
        return v
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'new_password' in info.data and v.get_secret_value() != info.data['new_password'].get_secret_value():
            raise ValueError('New password and confirmation password do not match')
        return v
    


class User(BaseModel):
    id: bson.ObjectId
    email: EmailStr
    username: str
    password: str
    is_verified: bool
    email_notifications: bool = True

    class Config:
        arbitrary_types_allowed = True

class NewUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    is_verified: bool = False

class NotificationSettings(BaseModel):
    email_notifications: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: SecretStr
    confirm_password: SecretStr
    
    @field_validator('otp')
    @classmethod
    def validate_otp(cls, v):
        return validate_otp_format(v)
    
    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v):
        password = v.get_secret_value()
        validate_password_strength(password)
        return v
    
    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, v, info):
        if 'new_password' in info.data and v.get_secret_value() != info.data['new_password'].get_secret_value():
            raise ValueError('New password and confirmation password do not match')
        return v