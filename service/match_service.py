import bson
from fastapi import HTTPException
from crud.match_crud import get_match_by_id, update_match_status, get_matches_by_user, update_match_by
from schemas.match_schema import MatchStatusUpdate, Match, MatchResponse
from schemas.user_schema import User
from service.upload_service import generate_download_url


def change_match_status(match_status: MatchStatusUpdate):
    is_updated = update_match_status(match_status.match_id, match_status.status)
    if not is_updated:
        raise HTTPException(status_code=404, detail="Match not found")


def match_is_analyzed(match_id: str):
    is_updated = update_match_by({'_id': bson.ObjectId(match_id)}, {"is_analyzed": True})
    if not is_updated:
        raise HTTPException(status_code=404, detail="Match not found")


def match_is_annotated(match_id: str):
    is_updated = update_match_by({'_id': bson.ObjectId(match_id)}, {"is_annotated": True})
    if not is_updated:
        raise HTTPException(status_code=404, detail="Match not found")


def get_matches(user: User):
    matches = get_matches_by_user(str(user.id))
    return matches


def get_user_match(match_id: str, user: User) -> Match:
    match = get_match_by_id(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return match


def generate_match_response(match: Match) -> MatchResponse:
    match_dict = match.model_dump()
    match_dict["video_url"] = generate_download_url(match.video_id)
    if match.is_annotated:
        match_dict["annotated_video_url"] = generate_download_url(f"{match.video_id}_annotated")
    if match.is_analyzed:
        match_dict["analysis_data_url"] = generate_download_url(f"{match.video_id}_data")
    return MatchResponse(**match_dict)
