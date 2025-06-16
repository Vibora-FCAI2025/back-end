import bson
from pydantic import BaseModel, EmailStr, SecretStr

class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: SecretStr

class UserLogin(BaseModel):
    email: EmailStr
    password: SecretStr

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