import bson
from pydantic import BaseModel, EmailStr, SecretStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr

class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr

class OTPVerify(BaseModel):
    email: EmailStr
    otp: SecretStr

class User(BaseModel):
    id: bson.ObjectId
    email: EmailStr
    username: str
    password: SecretStr
    is_verified: bool

    class Config:
        arbitrary_types_allowed = True
