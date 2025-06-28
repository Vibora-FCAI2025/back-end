from datetime import datetime, timedelta
from jose import JWTError, jwt

from config import get_settings

settings = get_settings()


def create_access_token(data: dict, expires_delta: timedelta | None = None, *, use_internal=False) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=settings.jwt_expire_minutes))
    to_encode.update({"exp": expire})
    secret = settings.internal_jwt_secret_key if use_internal else settings.jwt_secret_key
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_access_token(token: str, *, use_internal=False) -> dict:
    secret = settings.internal_jwt_secret_key if use_internal else settings.jwt_secret_key
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e
