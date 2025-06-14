from typing import List
from models.user import User, UserCreate, UserUpdate

fake_db = []

def get_user_by_id(user_id: int) -> User:
    return next((user for user in fake_db if user.id == user_id), None)

def get_all_users() -> List[User]:
    return fake_db

def create_user(user: UserCreate) -> User:
    new_user = User(id=len(fake_db) + 1, **user.dict())
    fake_db.append(new_user)
    return new_user

def update_user(user_id: int, user: UserUpdate) -> User:
    db_user = get_user_by_id(user_id)
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        return db_user
    return None

def delete_user(user_id: int) -> bool:
    db_user = get_user_by_id(user_id)
    if db_user:
        fake_db.remove(db_user)
        return True
    return False
