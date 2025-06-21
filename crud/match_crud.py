from pymongo.collection import Collection
from bson import ObjectId
from typing import Optional, List, Literal
from database import database
from schemas.match_schema import MatchCreate, Match, MatchStatusUpdate
from datetime import datetime

match_collection: Collection = database.get_collection("matches")


def create_match(data: MatchCreate) -> str:
    match_dict = data.model_dump()
    match_dict["date"] = match_dict.get("date", datetime.now())
    result = match_collection.insert_one(match_dict)
    return str(result.inserted_id)


def get_match_by_id(match_id: str) -> Optional[Match]:
    match = match_collection.find_one({"_id": ObjectId(match_id)})
    if match:
        return Match(**match)
    return None


def get_matches_by_user(user_id: str) -> List[Match]:
    matches = match_collection.find({"user_id": user_id})
    return [Match(**m) for m in matches]


def update_match_status(match_id: str, new_status: Literal["queued", "processing", "finished"]) -> bool:
    result = match_collection.update_one(
        {"_id": ObjectId(match_id)},
        {"$set": {"status": new_status}},
    )
    return result.modified_count > 0


def delete_match(match_id: str) -> bool:
    result = match_collection.delete_one({"_id": ObjectId(match_id)})
    return result.deleted_count > 0
