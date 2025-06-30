import random
from utils.email import send_otp_email
from schemas.otp_schema import OTPVerify
from crud.otp_crud import create_otp, get_otp, delete_otp
from crud.user_crud import create_user

OTP_RANGE_LOW = 100000
OTP_RANGE_HIGH = 999999


def generate_otp() -> str:
    otp = str(random.randint(OTP_RANGE_LOW, OTP_RANGE_HIGH))
    return otp


def send_otp(email: str):
    otp = generate_otp()
    create_otp(email, otp)
    send_otp_email(email, otp)


def verify_otp(email: str, otp: str) -> bool:
    saved_otp = get_otp(email)
    if saved_otp and saved_otp == otp:
        delete_otp(email)
        return True
    return False
