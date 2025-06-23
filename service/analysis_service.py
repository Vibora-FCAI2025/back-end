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
        date=datetime.now(),
        video_url=generate_download_url(analysis.video_id)
    )

    match_id = create_match(match_create)
    match = get_match_by_id(match_id)
    send_analysis_request(match, analysis.keypoints)

    return match_id


def send_analysis_request(match: Match, keypoints: List[List[int]]) -> dict:
    token = create_access_token(
        {"iss": "backend", "aud": "cli", "scope": "internal"},
        use_internal=True
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = f"{settings.analysis_cli_server}:{settings.analysis_cli_port}/analyze"

    response = requests.post(
        url,
        headers=headers,
        json={
            "user_id": str(match.user_id),
            "video_id": str(match.video_id),
            "video_path": match.video_url,
            "court_points": keypoints
        },
        timeout=10
    )

    response.raise_for_status()
    return response.json()
