from schemas.user_schema import UserRegister, NewUser, UserLogin, ChangePassword, ForgotPasswordRequest, ResetPasswordRequest
from schemas.otp_schema import OTPVerify
from utils.auth import hash_password, verify_password
from utils.jwt import create_access_token
from fastapi import HTTPException, status
from crud.user_crud import create_user, get_user_by_email, get_user_by_id, update_user_password, verify_user
from service.otp_service import send_otp, verify_otp


def check_user_exists(email: str):
    existing_user = get_user_by_email(email)
    if existing_user:
        return True
    return False


def initiate_signup(user_data: UserRegister):
    if check_user_exists(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    hashed_user = NewUser(
        email=user_data.email,
        username=user_data.username,
        password=hash_password(user_data.password.get_secret_value())
    )
    create_user(hashed_user)
    send_otp(user_data.email)


def login_user(user_data: UserLogin):
    user = get_user_by_email(user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not verified"
        )

    if not verify_password(user_data.password.get_secret_value(), user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return create_access_token({"sub": str(user.id)})


def change_password(user_id: str, password_data: ChangePassword):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify current password
    if not verify_password(password_data.current_password.get_secret_value(), user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Hash the new password
    new_hashed_password = hash_password(password_data.new_password.get_secret_value())
    
    # Update password in database
    success = update_user_password(user_id, new_hashed_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password"
        )
    
    return {"message": "Password changed successfully"}


def initiate_forgot_password(forgot_request: ForgotPasswordRequest):
    """Initiate forgot password process by sending OTP to user's email"""
    user = get_user_by_email(forgot_request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not verified"
        )
    
    send_otp(forgot_request.email)
    return {"message": "Password reset OTP sent to your email"}


def reset_password(reset_request: ResetPasswordRequest):
    """Reset user password using OTP verification"""
    # Verify the user exists
    user = get_user_by_email(reset_request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify OTP
    if not verify_otp(reset_request.email, reset_request.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Hash the new password
    new_hashed_password = hash_password(reset_request.new_password.get_secret_value())
    
    # Update password in database
    success = update_user_password(str(user.id), new_hashed_password)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password"
        )
    
    return {"message": "Password reset successfully"}


def verify_user_with_otp(data: OTPVerify):
    """Verify OTP and mark user as verified"""
    if verify_otp(data.email, data.otp):
        verify_user(data.email)
        return {"message": "User registered successfully"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid OTP"
    )