import bson
from typing import List
from fastapi import APIRouter, Depends
from dependencies.auth import is_auth
from dependencies.internal import is_internal
from schemas.match_schema import MatchStatusUpdate, MatchAnalysisRequest, Match, MatchResponse
from schemas.user_schema import User
from service.analysis_service import analyze_match
from service.match_service import change_match_status, get_matches, get_user_match, generate_match_response
from service.upload_service import generate_upload_url

router = APIRouter()


@router.get("/get-upload")
def get_upload(user: User = Depends(is_auth)):
    video_id = bson.ObjectId()
    upload_url = generate_upload_url(video_id)
    return {"upload-url": upload_url,
            "video_id": video_id}


@router.post("/update-status", responses={
    401: {"description": "Unauthorized Access"}
})
def update_status(video_data: MatchStatusUpdate, auth=Depends(is_internal)):
    change_match_status(video_data)
    return "Status changed successfully"


@router.post("/analyse_video")
def analyse_video(match: MatchAnalysisRequest, user: User = Depends(is_auth)):
    match_id = analyze_match(match, user)
    return {"match_id": match_id}


@router.get("/match_history", response_model=List[MatchResponse])
def get_match_history(user: User = Depends(is_auth)):
    matches = get_matches(user)
    return [MatchResponse(**match.model_dump()) for match in matches]


@router.get("/match/{match_id}", response_model=MatchResponse)
def get_match(match_id: str, user: User = Depends(is_auth)):
    match = get_user_match(match_id, user)
    return  generate_match_response(match)
