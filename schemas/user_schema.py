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
    otp: str

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