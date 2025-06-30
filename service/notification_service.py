from schemas.user_schema import NotificationSettings
from fastapi import HTTPException, status
from crud.user_crud import update_user_by, get_user_by_id
from utils.email import send_email
import bson


def update_email_notifications(user_id: str, settings: NotificationSettings):
    """Update user's email notification preference"""
    success = update_user_by(
        {"_id": bson.ObjectId(user_id)}, 
        {"email_notifications": settings.email_notifications}
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update notification settings"
        )
    return {"message": "Notification settings updated successfully"}


def notify_user(user_id: str, message: str, subject: str = "Notification"):
    """Notify user via all enabled notification methods"""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    notifications_sent = []
    
    # Send email notification if enabled
    if user.email_notifications:
        email_sent = send_email(user.email, subject, message)
        if email_sent:
            notifications_sent.append("email")
    
    # Future notification types can be added here
    # if user.sms_notifications:
    #     sms_sent = send_sms(user.phone, message)
    #     if sms_sent:
    #         notifications_sent.append("sms")
    
    return {
        "message": "Notification sent successfully",
        "methods": notifications_sent,
        "user_id": user_id
    } 