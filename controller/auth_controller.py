from fastapi import APIRouter, Depends, HTTPException, Request
from schemas.user_schema import UserRegister, UserLogin, TokenResponse, ChangePassword, User, ForgotPasswordRequest, ResetPasswordRequest
from schemas.otp_schema import OTPVerify
from service import auth_service, otp_service
from dependencies.auth import is_auth
import json

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
async def change_password(
    request: Request,
    current_user: User = Depends(is_auth)
):
    try:
        # Get the request body
        body = await request.body()
        
        # Decode if it's bytes
        if isinstance(body, bytes):
            body_str = body.decode('utf-8')
        else:
            body_str = str(body)
        
        # Parse JSON
        try:
            data = json.loads(body_str)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")
        
        # Create ChangePassword object
        password_data = ChangePassword(
            current_password=data.get("current_password"),
            new_password=data.get("new_password"),
            confirm_password=data.get("confirm_password")
        )
        
        return auth_service.change_password(str(current_user.id), password_data)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in change_password: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing request: {str(e)}")





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



