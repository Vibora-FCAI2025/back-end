from schemas.user_schema import UserRegister, NewUser, UserLogin
from utils.auth import hash_password, verify_password
from utils.jwt import create_access_token
from fastapi import HTTPException, status
from crud.user_crud import create_user, get_user_by_email
from service.otp_service import send_otp


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