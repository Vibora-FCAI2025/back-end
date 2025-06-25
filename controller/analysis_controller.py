import bson
from fastapi import APIRouter, Depends

from dependencies.auth import is_auth
from schemas.match_schema import MatchAnalysisRequest
from schemas.user_schema import User
from service.analysis_service import analyze_match
from service.upload_service import generate_upload_url

router = APIRouter()


@router.get("/get-upload")
def get_upload(user: User = Depends(is_auth)):
    video_id = bson.ObjectId()
    upload_url = generate_upload_url(video_id)
    return {"upload-url": upload_url,
            "video_id": str(video_id)}


@router.post("/analyze_video")
def analyse_video(match: MatchAnalysisRequest, user: User = Depends(is_auth)):
    match_id = analyze_match(match, user)
    return {"match_id": match_id}
