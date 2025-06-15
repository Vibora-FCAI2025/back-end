from http.client import HTTPException
from fastapi import APIRouter
from schemas.user_schema import UserCreate, UserLogin
from schemas.otp_schema import OTPVerify
from service import auth_service, otp_service
from fastapi import HTTPException

router = APIRouter()


@router.post("/register")
def register(user: UserCreate):
    otp = auth_service.initiate_signup(user)
    return {"message": "OTP sent to your email"}


@router.post("/verify-otp")
async def verify_otp(data: OTPVerify):
    if otp_service.verify_otp(data):
        return {"message": "User registered successfully"}
    raise HTTPException(status_code=400, detail="Invalid OTP")


@router.post("/login")
def login(user: UserLogin):
    auth_service.login_user(user)
    return {"message": "Login successful"}