from datetime import datetime
from typing import List

import requests
from bson import ObjectId

from config import get_settings
from crud.match_crud import create_match, get_match_by_id
from schemas.match_schema import MatchAnalysisRequest, MatchCreate, Match
from schemas.user_schema import User
from service.upload_service import generate_download_url
from utils.jwt import create_access_token

settings = get_settings()


def analyze_match(analysis: MatchAnalysisRequest, user: User):
    match_create = MatchCreate(
        video_id=ObjectId(analysis.video_id),
        user_id=user.id,
        date=datetime.now()
    )

    match_id = create_match(match_create)
    send_analysis_request(match_id, analysis.video_id, user.id, analysis.keypoints)

    return match_id


def send_analysis_request(match_id: str, video_id: str, user_id, keypoints: List[List[int]]) -> dict:
    token = create_access_token({}, use_internal=True)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = f"http://{settings.analysis_cli_server}:{settings.analysis_cli_port}/analyze"

    response = requests.post(
        url,
        headers=headers,
        json={
            "user_id": str(user_id),
            "match_id": str(match_id),
            "video_id": str(video_id),
            "video_path": generate_download_url(video_id),
            "court_points": keypoints
        },
        timeout=10
    )

    response.raise_for_status()
    return response.json()
