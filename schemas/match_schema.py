from datetime import datetime

import bson
from pydantic import BaseModel, field_serializer
from typing import Literal, List, Optional

MATCH_STATUS = Literal["pending", "queued", "processing", "finished"]


class MatchStatusUpdate(BaseModel):
    match_id: str
    status: MATCH_STATUS


class MatchAnalysisRequest(BaseModel):
    video_id: str
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

    class Config:
        arbitrary_types_allowed = True

    @field_serializer('id')
    def serialize_id(self, value: bson.ObjectId) -> str:
        return str(value)

class MatchResponse(BaseModel):
    id: str
    status: MATCH_STATUS
    video_url: str


class MatchCreate(BaseModel):
    video_id: bson.ObjectId
    user_id: bson.ObjectId
    date: datetime
    video_url: str

    class Config:
        arbitrary_types_allowed = True
