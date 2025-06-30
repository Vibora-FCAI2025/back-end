from fastapi import APIRouter, Depends, HTTPException
from schemas.user_schema import UserRegister, UserLogin, TokenResponse, ChangePassword, User
from schemas.otp_schema import OTPVerify
from service import auth_service, otp_service
from dependencies.auth import is_auth

router = APIRouter()


@router.post("/register")
def register(user: UserRegister):
    otp = auth_service.initiate_signup(user)
    return {"message": "OTP sent to your email"}


@router.post("/verify-otp")
async def verify_otp(data: OTPVerify):
    if otp_service.verify_otp(data):
        return {"message": "User registered successfully"}
    raise HTTPException(status_code=400, detail="Invalid OTP")


@router.post("/login", response_model=TokenResponse, responses={
    401: {"description": "Invalid credentials"},
    403: {"description": "User not verified"},
    404: {"description": "User not found"}
})
def login(user: UserLogin):
    token = auth_service.login_user(user)
    return {"access_token": token, "token_type": "bearer"}


@router.put("/change-password", responses={
    200: {"description": "Password changed successfully"},
    400: {"description": "Current password is incorrect or validation error"},
    401: {"description": "Unauthorized"},
    404: {"description": "User not found"},
    500: {"description": "Failed to update password"}
})
def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(is_auth)
):
    return auth_service.change_password(str(current_user.id), password_data)
