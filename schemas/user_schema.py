import bson
from pydantic import BaseModel, EmailStr, SecretStr, field_validator

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr

class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr

class ChangePassword(BaseModel):
    current_password: SecretStr
    new_password: SecretStr
    confirm_password: SecretStr
    
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

    class Config:
        arbitrary_types_allowed = True

class NewUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    is_verified: bool = False

class TokenResponse(BaseModel):
    access_token: str
    token_type: str