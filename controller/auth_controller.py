from http.client import HTTPException
from fastapi import APIRouter
from crud.user_crud import get_user_by_email
from schemas.user_schema import UserCreate, UserLogin
from schemas.otp_schema import OTPVerify
from service import auth_service
from fastapi import HTTPException

router = APIRouter()


@router.post("/register")
def register(user: UserCreate):
    otp = auth_service.initiate_signup(user)
    return {"message": "OTP sent to your email"}


@router.post("/verify-otp")
async def verify_otp(data: OTPVerify):
    if auth_service.verify_otp(data):
        return {"message": "User registered successfully"}
    raise HTTPException(status_code=400, detail="Invalid OTP")


@router.post("/login")
def login(user: UserLogin):
    record = get_user_by_email(user.email)
    if not record:
        raise HTTPException(status_code=404, detail="User not found")

    if not auth_service.verify_password(user.password.get_secret_value(), record["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}