import random
from utils.email import send_otp_email
from schemas.user_schema import UserCreate, NewUser
from schemas.otp_schema import OTPVerify
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from crud.user_crud import create_user, verify_user
from crud.otp_crud import create_otp, get_otp, delete_otp


def initiate_signup(user_data: UserCreate) -> str:
    hashed_user = NewUser(
        email=user_data.email,
        username=user_data.username,
        password=hash_password(user_data.password.get_secret_value())
    )
    create_user(hashed_user)

    otp = str(random.randint(100000, 999999))
    create_otp(user_data.email, otp)

    send_otp_email(user_data.email, otp)
    return otp


def verify_otp(data: OTPVerify) -> bool:
    saved_otp = get_otp(data.email)
    if saved_otp and saved_otp == data.password:
        verify_user(data.email)
        delete_otp(data.email)
        return True
    return False


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # print("Hashed password from DB:", hashed_password)
    # print("Plain password from user:", plain_password)

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        # Log the issue and return False
        print("Invalid hash format detected")
        return False
