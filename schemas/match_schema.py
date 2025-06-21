from datetime import datetime

import bson
from pydantic import BaseModel
from typing import Any, Literal, List, Optional


class MatchStatusUpdate(BaseModel):
    match_id: bson.ObjectId
    status: Literal["queued", "processing", "finished"]

class MatchResponse(BaseModel):
    id: bson.ObjectId
    data: Any
    annotated_video_url: str

class MatchAnalysisRequest(BaseModel):
    video_id: bson.ObjectId
    keypoints: List[List[int, int]]

class Match(BaseModel):
    id: bson.ObjectId
    video_id: bson.ObjectId
    user_id: bson.ObjectId
    date: datetime
    status: Literal["queued", "processing", "finished"]
    video_url: Optional[str] = None
    annotated_url: Optional[str] = None
    data_url: Optional[str] = None

class MatchCreate(BaseModel):
    video_id: bson.ObjectId
    user_id: bson.ObjectId
    date: datetime