from pydantic import BaseModel, EmailStr, field_validator
from utils.validation import validate_otp_format


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str
    
    @field_validator('otp')
    @classmethod
    def validate_otp(cls, v):
        return validate_otp_format(v)
