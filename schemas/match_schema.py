from datetime import datetime

import bson
from pydantic import BaseModel
from typing import Any, Literal, List, Optional

MATCH_STATUS = Literal["pending", "queued", "processing", "finished"]

class MatchStatusUpdate(BaseModel):
    match_id: bson.ObjectId
    status: MATCH_STATUS

class MatchAnalysisRequest(BaseModel):
    video_id: bson.ObjectId
    keypoints: List[List[int, int]]

class Match(BaseModel):
    id: bson.ObjectId
    video_id: bson.ObjectId
    user_id: bson.ObjectId
    date: datetime
    status: MATCH_STATUS
    video_url: str
    annotated_url: Optional[str] = None
    data_url: Optional[str] = None

class MatchCreate(BaseModel):
    video_id: bson.ObjectId
    user_id: bson.ObjectId
    date: datetime
    video_url: str