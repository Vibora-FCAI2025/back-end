from bson import ObjectId
from typing import Optional, List, Dict, Any
from database import database
from schemas.match_schema import MatchCreate, Match, MATCH_STATUS
from datetime import datetime

match_collection = database.get_collection("matches")


def create_match(data: MatchCreate) -> str:
    match_dict = data.model_dump()
    match_dict["date"] = match_dict.get("date", datetime.now())
    match_dict["status"] = "pending"
    result = match_collection.insert_one(match_dict)
    return str(result.inserted_id)


def find_match_by(filters: Dict[str, Any]) -> Optional[Match]:
    match_doc = match_collection.find_one(filters)
    if match_doc:
        return Match(
            id=match_doc["_id"],
            date=match_doc["date"],
            video_id=match_doc["video_id"],
            user_id=match_doc["user_id"],
            video_url=match_doc["video_url"],
            status=match_doc["status"],
            annotated_url=match_doc.get("annotated_url", None),
            data_url=match_doc.get("data_url", None),
        )
    return None


def update_match_by(filters: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
    result = match_collection.update_one(filters, {"$set": update_data})
    return result.modified_count > 0


def find_all_match_by(filters: Dict[str, Any]) -> List[Match]:
    matches_docs = match_collection.find(filters)
    matches = []
    for match_doc in matches_docs:
        match = Match(
            id=match_doc["_id"],
            date=match_doc["date"],
            video_id=match_doc["video_id"],
            user_id=match_doc["user_id"],
            video_url=match_doc["video_url"],
            status=match_doc["status"],
            annotated_url=match_doc.get("annotated_url", None),
            data_url=match_doc.get("data_url", None),
        )
        matches.append(match)
    return matches


def get_match_by_id(match_id: str) -> Optional[Match]:
    return find_match_by({"_id": ObjectId(match_id)})


def get_matches_by_user(user_id: str) -> List[Match]:
    return find_all_match_by({"user_id": user_id})


def update_match_status(match_id: str, new_status: MATCH_STATUS) -> bool:
    return update_match_by(
        {"_id": ObjectId(match_id)},
        {"status": new_status},
    )


def delete_match(match_id: str) -> bool:
    result = match_collection.delete_one({"_id": ObjectId(match_id)})
    return result.deleted_count > 0
