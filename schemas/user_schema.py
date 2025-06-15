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
    