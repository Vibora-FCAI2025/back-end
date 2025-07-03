from datetime import datetime

import bson
from pydantic import BaseModel, field_serializer, field_validator
from typing import Literal, List, Optional
from utils.validation import validate_object_id, validate_title_length, validate_keypoints_structure

MATCH_STATUS = Literal["pending", "queued", "processing", "finished"]


class MatchStatusUpdate(BaseModel):
    match_id: str
    status: MATCH_STATUS
    notify: bool = True
    
    @field_validator('match_id')
    @classmethod
    def validate_match_id(cls, v):
        return validate_object_id(v)


class MatchAnalysisRequest(BaseModel):
    video_id: str
    title: str
    keypoints: List[List[int]]
    
    @field_validator('video_id')
    @classmethod
    def validate_video_id(cls, v):
        return validate_object_id(v)
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        return validate_title_length(v)
    
    @field_validator('keypoints')
    @classmethod
    def validate_keypoints(cls, v):
        return validate_keypoints_structure(v)


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
    
    @field_validator('match_id')
    @classmethod
    def validate_match_id(cls, v):
        return validate_object_id(v)


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
