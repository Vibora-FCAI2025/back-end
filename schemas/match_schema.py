import bson
from pydantic import BaseModel
from typing import Any, Literal, List


class VideoStatusUpdate(BaseModel):
    video_id: str
    status: Literal["queued", "processing", "finished"]

class MatchResponse(BaseModel):
    id: int
    data: Any
    annotated_video_url: str

class MatchAnalysisRequest(BaseModel):
    video_id: bson.ObjectId
    keypoints: List[List[int, int]]
