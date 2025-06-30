from fastapi import APIRouter, Depends
from schemas.user_schema import User, NotificationSettings
from service import notification_service
from dependencies.auth import is_auth

router = APIRouter()


@router.put("/notification-settings")
def toggle_email_notifications(
    settings: NotificationSettings,
    current_user: User = Depends(is_auth)
):
    return notification_service.update_email_notifications(str(current_user.id), settings) 