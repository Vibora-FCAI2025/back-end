import random
from utils.email import send_otp_email
from schemas.user_schema import UserCreate
from schemas.user_schema import OTPVerify
from database import database
from passlib.context import CryptContext
from passlib.exc import UnknownHashError


otp_collection = database.get_collection("otp")
user_collection = database.get_collection("users")
# service/auth_service.py (or wherever you keep your service logic)


def initiate_signup(user_data: UserCreate):
    otp = str(random.randint(100000, 999999))

    user_data_dict = user_data.model_dump()
    user_data_dict["password"] = hash_password(user_data.password.get_secret_value())

    otp_collection.insert_one({
    "email": user_data.email,
    "otp": otp,
    "data": user_data_dict
})


    send_otp_email(user_data.email, otp)
    return otp

def verify_otp(data: OTPVerify):
    record = otp_collection.find_one({"email": data.email, "otp": data.otp})
    if record:
        user_collection.insert_one(record["data"])
        otp_collection.delete_one({"_id": record["_id"]})
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
