from typing import List
from fastapi import APIRouter, Depends
from dependencies.auth import is_auth
from dependencies.internal import is_internal
from schemas.match_schema import MatchStatusUpdate, MatchResponse
from schemas.user_schema import User
from service.match_service import change_match_status, get_matches, get_user_match, generate_match_response, \
    match_is_analyzed, match_is_annotated

router = APIRouter()


@router.post("/update-status", responses={
    401: {"description": "Unauthorized Access"}
})
def update_status(video_data: MatchStatusUpdate, auth=Depends(is_internal)):
    change_match_status(video_data)
    return "Status changed successfully"


@router.get("/match_history", response_model=List[MatchResponse])
def get_match_history(user: User = Depends(is_auth)):
    matches = get_matches(user)
    return [generate_match_response(match) for match in matches]


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: str, user: User = Depends(is_auth)):
    match = get_user_match(match_id, user)
    return  generate_match_response(match)

@router.post("/analyzed")
def mark_match_as_analyzed(data: dict, auth=Depends(is_internal)):
    match_id = data["match_id"]
    match_is_analyzed(match_id)
    return 200

@router.post("/annotated")
def mark_match_as_annotated(data: dict, auth=Depends(is_internal)):
    match_id = data["match_id"]
    match_is_annotated(match_id)
    return 200