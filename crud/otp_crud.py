from typing import Optional
from pymongo.errors import PyMongoError
from database import database

otp_collection = database.get_collection("otp")


def create_otp(email: str, otp_code: str) -> bool:
    otp_collection.update_one(
        {"email": email},
        {"$set": {"otp": otp_code}},
        upsert=True
    )
    return True


def get_otp(email: str) -> Optional[str]:
    doc = otp_collection.find_one({"email": email})
    return doc.get("otp") if doc else None


def delete_otp(email: str) -> bool:
    result = otp_collection.delete_one({"email": email})
    return result.deleted_count > 0
