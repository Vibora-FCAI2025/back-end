from schemas.user_schema import UserCreate, NewUser
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
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
