from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from dependencies.auth import is_auth
from dependencies.internal import is_internal
from schemas.match_schema import MatchStatusUpdate, MatchResponse, MatchID, PaginatedMatchResponse
from schemas.user_schema import User
from service.match_service import change_match_status, get_matches, get_user_match, generate_match_response, \
    match_is_analyzed, match_is_annotated, match_screenshot_generated, get_paginated_matches
from utils.validation import validate_object_id

router = APIRouter()


@router.post("/update-status", responses={
    401: {"description": "Unauthorized Access"}
})
def update_status(video_data: MatchStatusUpdate, auth=Depends(is_internal)):
    change_match_status(video_data)
    return "Status changed successfully"


@router.get("/match_history", response_model=PaginatedMatchResponse)
def get_match_history(
    user: User = Depends(is_auth),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page (1-100)")
):
    return get_paginated_matches(user, page, limit)


@router.get("/match_history/all", response_model=List[MatchResponse])
def get_all_match_history(user: User = Depends(is_auth)):
    matches = get_matches(user)
    return [generate_match_response(match) for match in matches]


@router.get("/{match_id}", response_model=MatchResponse)
def get_match(match_id: str, user: User = Depends(is_auth)):
    # Validate match_id format before processing using centralized validation
    try:
        validate_object_id(match_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    match = get_user_match(match_id, user)
    return  generate_match_response(match)

@router.post("/analyzed")
def mark_match_as_analyzed(match: MatchID, auth=Depends(is_internal)):
    match_id = match.match_id
    match_is_analyzed(match_id)
    return 200

@router.post("/annotated")
def mark_match_as_annotated(match: MatchID, auth=Depends(is_internal)):
    match_id = match.match_id
    match_is_annotated(match_id)
    return 200

@router.post("/screenshot-generated")
def mark_match_screenshot_generated(match: MatchID, auth=Depends(is_internal)):
    match_id = match.match_id
    match_screenshot_generated(match_id)
    return 200