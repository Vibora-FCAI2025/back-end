from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.jwt import decode_access_token
from crud.user_crud import get_user_by_id
from schemas.user_schema import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def is_auth(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_access_token(token)
        
        # Check for token expiry
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(status_code=401, detail="Token missing expiration")
        
        # Convert exp to datetime and check if expired
        exp_datetime = datetime.fromtimestamp(exp)
        if datetime.now() > exp_datetime:
            raise HTTPException(status_code=401, detail="Token has expired")
        
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Token missing subject")

        user = get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
