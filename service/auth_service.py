from schemas.user_schema import UserCreate, NewUser
from utils.auth import hash_password
from crud.user_crud import create_user
from service.otp_service import send_otp


def initiate_signup(user_data: UserCreate):
    hashed_user = NewUser(
        email=user_data.email,
        username=user_data.username,
        password=hash_password(user_data.password.get_secret_value())
    )
    create_user(hashed_user)
    send_otp(user_data.email)
