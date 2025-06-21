from fastapi import HTTPException
from crud.match_crud import get_match_by_id, update_match_status, get_matches_by_user
from schemas.match_schema import MatchStatusUpdate, Match
from schemas.user_schema import User


def change_match_status(match_status: MatchStatusUpdate, user: User):
    match = get_match_by_id(str(match_status.match_id))
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.user_id != user.id:
        raise HTTPException(status_code=401, detail="Unauthorized Access")
    update_match_status(str(match_status.match_id), match_status.status)


def get_matches(user: User):
    matches = get_matches_by_user(str(user.id))
    return matches


# In services/match_service.py
def get_user_match(match_id: str, user_id: str) -> Match:
    match = get_match_by_id(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return match
