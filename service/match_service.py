import bson
from fastapi import HTTPException
from crud.match_crud import get_match_by_id, update_match_status, get_matches_by_user, update_match_by
from schemas.match_schema import MatchStatusUpdate, Match, MatchResponse
from schemas.user_schema import User
from service.upload_service import generate_download_url
from service.notification_service import notify_user


def change_match_status(match_status: MatchStatusUpdate):
    is_updated = update_match_status(match_status.match_id, match_status.status)
    if not is_updated:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Send notification to the user only if notify_user is True
    if match_status.notify:
        match = get_match_by_id(match_status.match_id)
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        
        try:
            message = f"Your match '{match.title}' status has been updated to {match_status.status}."
            subject = f"Match Status Update: {match.title}"
            
            notify_user(str(match.user_id), message, subject)
        except Exception as e:
            # Log the error but don't fail the status update
            print(f"Failed to send notification for match {match_status.match_id}: {str(e)}")


def match_is_analyzed(match_id: str):
    is_updated = update_match_by({'_id': bson.ObjectId(match_id)}, {"is_analyzed": True})
    if not is_updated:
        raise HTTPException(status_code=404, detail="Match not found")


def match_is_annotated(match_id: str):
    is_updated = update_match_by({'_id': bson.ObjectId(match_id)}, {"is_annotated": True})
    if not is_updated:
        raise HTTPException(status_code=404, detail="Match not found")


def match_screenshot_generated(match_id: str):
    is_updated = update_match_by({'_id': bson.ObjectId(match_id)}, {"is_screenshot_generated": True})
    if not is_updated:
        raise HTTPException(status_code=404, detail="Match not found")


def get_matches(user: User):
    matches = get_matches_by_user(str(user.id))
    return matches


def get_user_match(match_id: str, user: User) -> Match:
    match = get_match_by_id(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return match


def generate_match_response(match: Match) -> MatchResponse:
    resp = MatchResponse(
        id=str(match.id),
        title=match.title,
        status=match.status,
        date=match.date,
        video_url=generate_download_url(str(match.video_id) + ".mp4"),
        match_screenshot_url=None,
        annotated_video_url=None,
        analysis_data_url=None
    )
    if match.is_screenshot_generated:
        resp.match_screenshot_url = generate_download_url(f"{match.video_id}_screenshot.jpg")
    if match.is_annotated:
        resp.annotated_video_url = generate_download_url(f"{match.video_id}_annotated.mp4")
    if match.is_analyzed:
        resp.analysis_data_url = generate_download_url(f"{match.video_id}_data.csv")
    return  resp
