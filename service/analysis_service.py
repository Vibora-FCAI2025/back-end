from datetime import datetime

from crud.match_crud import create_match
from schemas.match_schema import MatchAnalysisRequest, MatchCreate
from schemas.user_schema import User
from service.upload_service import generate_download_url


def analyze_match(match: MatchAnalysisRequest, user: User):
    match_create = MatchCreate(
        video_id=match.video_id,
        user_id=user.user_id,
        date=datetime.now(),
        download_url=generate_download_url(match.video_id)
    )

    match_id = create_match(match_create)

    # send analysis request

    return match_id

