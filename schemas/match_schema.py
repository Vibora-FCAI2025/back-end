from datetime import datetime

import bson
from pydantic import BaseModel, field_serializer
from typing import Literal, List, Optional

MATCH_STATUS = Literal["pending", "queued", "processing", "finished"]


class MatchStatusUpdate(BaseModel):
    match_id: str
    status: MATCH_STATUS
    notify: bool = True


class MatchAnalysisRequest(BaseModel):
    video_id: str
    title: str
    keypoints: List[List[int]]


class Match(BaseModel):
    id: bson.ObjectId
    video_id: bson.ObjectId
    user_id: bson.ObjectId
    title: str
    date: datetime
    status: MATCH_STATUS
    is_annotated: bool = False
    is_analyzed: bool = False
    is_screenshot_generated: bool = False

    class Config:
        arbitrary_types_allowed = True

    @field_serializer('id')
    def serialize_id(self, value: bson.ObjectId) -> str:
        return str(value)


class MatchResponse(BaseModel):
    id: str
    title: str
    status: MATCH_STATUS
    date: datetime
    video_url: str
    match_screenshot_url: Optional[str]
    annotated_video_url: Optional[str]
    analysis_data_url: Optional[str]


class PaginationMetadata(BaseModel):
    page: int
    limit: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedMatchResponse(BaseModel):
    matches: List[MatchResponse]
    pagination: PaginationMetadata


class MatchID(BaseModel):
    match_id: str


class UploadResponse(BaseModel):
    upload_url: str
    video_id: str


class MatchCreate(BaseModel):
    video_id: bson.ObjectId
    user_id: bson.ObjectId
    title: str
    date: datetime

    class Config:
        arbitrary_types_allowed = True
