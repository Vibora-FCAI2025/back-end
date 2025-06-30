from typing import Dict, Any, Optional
import bson
from database import database
from schemas.user_schema import User, NewUser

user_collection = database.get_collection("users")


def create_user(user_data: NewUser) -> bson.ObjectId:
    user_dict = {
        "email": user_data.email,
        "username": user_data.username,
        "password": user_data.password,
        "is_verified": False,
        "email_notifications": True
    }
    result = user_collection.insert_one(user_dict)
    return result.inserted_id


def find_user_by(filters: Dict[str, Any]) -> Optional[User]:
    user_doc = user_collection.find_one(filters)
    if user_doc:
        return User(
            id=user_doc["_id"],
            email=user_doc["email"],
            username=user_doc["username"],
            password=user_doc["password"],
            is_verified=user_doc.get("is_verified", False),
            email_notifications=user_doc.get("email_notifications", True)
        )
    return None


def update_user_by(filters: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
    result = user_collection.update_one(filters, {"$set": update_data})
    return result.modified_count > 0


def get_user_by_email(email: str) -> Optional[User]:
    return find_user_by({"email": email})


def get_user_by_id(user_id: str) -> Optional[User]:
    return find_user_by({"_id": bson.ObjectId(user_id)})


def update_user_by_email(email: str, update_data: Dict[str, Any]) -> bool:
    return update_user_by({"email": email}, update_data)


def verify_user(email: str) -> bool:
    return update_user_by_email(email, {"is_verified": True})


def update_user_password(user_id: str, new_password: str) -> bool:
    """Update user password by user ID"""
    return update_user_by({"_id": bson.ObjectId(user_id)}, {"password": new_password})
