from passlib.context import CryptContext
from passlib.exc import UnknownHashError

import bcrypt

if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('about', (object,), {'__version__': bcrypt.__version__})

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
