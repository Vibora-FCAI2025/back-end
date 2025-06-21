import bson
from fastapi import APIRouter, Depends
from dependencies.auth import is_auth
from schemas.match_schema import MatchResponse, MatchStatusUpdate, MatchAnalysisRequest
from schemas.user_schema import User
from service.upload_service import generate_upload_url, generate_download_url

router = APIRouter()


@router.get("/get-upload")
def get_upload(user: User = Depends(is_auth)):
    video_id = bson.ObjectId()
    upload_url = generate_upload_url(video_id)
    return {"upload-url": upload_url,
            "video_id": video_id}


@router.post("/update-status")
def update_status(video_data: MatchStatusUpdate, user: User = Depends(is_auth)):
    pass


@router.post("/analyse_video")
def analyse_video(match: MatchAnalysisRequest, user: User = Depends(is_auth)):
    # logic to analyze video
    return {"message": "Video analyzed"}


@router.get("/match_history", response_model=list[MatchResponse])
def get_match_history(user: User = Depends(is_auth)):
    # logic to return match history
    return []


@router.get("/match/{match_name}", response_model=MatchResponse)
def get_match(match_name: str, user: User = Depends(is_auth)):
    # logic to return specific match
    return {"id": 1, "data": {}, "annotated_video_url": "http://example.com/video.mp4"}
