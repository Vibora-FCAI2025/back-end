from fastapi import HTTPException
from crud.match_crud import get_match_by_id, update_match_status
from schemas.match_schema import MatchStatusUpdate
from schemas.user_schema import User


def change_match_status(match_status: MatchStatusUpdate, user: User):
    if get_match_by_id(str(match_status.match_id)).user_id == user.id:
        update_match_status(str(match_status.match_id), match_status.status)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized Access")
