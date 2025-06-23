from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from utils.jwt import decode_access_token

bearer_scheme = HTTPBearer(auto_error=True)


def is_internal(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    token = credentials.credentials

    try:
        payload = decode_access_token(token, use_internal=True)
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid token")

    return payload
