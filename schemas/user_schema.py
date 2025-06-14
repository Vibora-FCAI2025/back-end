from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str
    