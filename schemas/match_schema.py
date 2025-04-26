from pydantic import BaseModel
from typing import Any

class MatchResponse(BaseModel):
    id: int
    data: Any
    annotated_video_url: str
