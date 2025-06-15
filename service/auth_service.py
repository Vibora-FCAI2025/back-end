from schemas.user_schema import UserCreate, NewUser
from utils.auth import hash_password
from crud.user_crud import create_user
from fastapi import HTTPException, status
from crud.user_crud import create_user, get_user_by_email
from service.otp_service import send_otp


def check_user_exists(email: str):
    existing_user = get_user_by_email(email)
    if existing_user:
        return True
    return False


def initiate_signup(user_data: UserCreate):
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
