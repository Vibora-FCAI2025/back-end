from fastapi import APIRouter, UploadFile
from schemas.match_schema import MatchResponse

router = APIRouter()


@router.post("/analyse_video/")
def analyse_video(video_file: UploadFile):
    # logic to analyze video
    return {"message": "Video analyzed"}


@router.get("/match_history", response_model=list[MatchResponse])
def get_match_history():
    # logic to return match history
    return []


@router.get("/match/{match_name}", response_model=MatchResponse)
def get_match(match_name: str):
    # logic to return specific match
    return {"id": 1, "data": {}, "annotated_video_url": "http://example.com/video.mp4"}
