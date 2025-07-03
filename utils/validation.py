import re
import bson
from typing import Any


def validate_object_id(value: str) -> str:
    if not bson.ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId format')
    return value


def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters long')
    if len(password) > 128:
        raise ValueError('Password must be no more than 128 characters long')
    return password


def validate_username_format(username: str) -> str:
    if len(username) < 3:
        raise ValueError('Username must be at least 3 characters long')
    if len(username) > 30:
        raise ValueError('Username must be no more than 30 characters long')
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
    return username


def validate_otp_format(otp: str) -> str:
    if not otp.isdigit():
        raise ValueError('OTP must contain only digits')
    if len(otp) != 6:
        raise ValueError('OTP must be exactly 6 digits')
    return otp


def validate_title_length(title: str, max_length: int = 200) -> str:
    title = title.strip()
    if len(title) == 0:
        raise ValueError('Title cannot be empty')
    if len(title) > max_length:
        raise ValueError(f'Title must be no more than {max_length} characters long')
    return title


def validate_keypoints_structure(keypoints: list) -> list:
    if not keypoints:
        raise ValueError('Keypoints cannot be empty')
    
    for i, keypoint in enumerate(keypoints):
        if not isinstance(keypoint, list):
            raise ValueError(f'Keypoint {i} must be a list')
        if len(keypoint) != 2:
            raise ValueError(f'Keypoint {i} must contain exactly 2 coordinates (x, y)')
        if not all(isinstance(coord, int) and coord >= 0 for coord in keypoint):
            raise ValueError(f'Keypoint {i} coordinates must be non-negative integers')
    
    return keypoints 