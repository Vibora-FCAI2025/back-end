from fastapi import APIRouter, Depends, HTTPException
from schemas.user_schema import UserRegister, UserLogin, TokenResponse, ChangePassword, User, ForgotPasswordRequest, ResetPasswordRequest
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
    return auth_service.verify_user_with_otp(data)


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


@router.post("/forgot-password", responses={
    200: {"description": "Password reset OTP sent to email"},
    404: {"description": "User not found"},
    403: {"description": "User not verified"}
})
def forgot_password(forgot_request: ForgotPasswordRequest):
    return auth_service.initiate_forgot_password(forgot_request)


@router.post("/reset-password", responses={
    200: {"description": "Password reset successfully"},
    400: {"description": "Invalid or expired OTP, or password validation error"},
    404: {"description": "User not found"},
    500: {"description": "Failed to update password"}
})
def reset_password(reset_request: ResetPasswordRequest):
    return auth_service.reset_password(reset_request)



