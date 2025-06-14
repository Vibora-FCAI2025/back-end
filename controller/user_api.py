from http.client import HTTPException
from fastapi import APIRouter, UploadFile 
from schemas.user_schema import UserCreate, UserLogin
from schemas.match_schema import MatchResponse
from service import auth_service
from fastapi import HTTPException
from schemas.user_schema import OTPVerify




router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    otp = auth_service.initiate_signup(user)
    return {"message": "OTP sent to your email"}

    
@router.post("/verify-otp")
async def verify_otp(data: OTPVerify):
    if auth_service.verify_otp(data):
        return {"message": "User registered successfully"}
    raise HTTPException(status_code=400, detail="Invalid OTP")



@router.post("/login")
def login(user: UserLogin):
   record =auth_service.user_collection.find_one({"email": user.email})
   if not record:
        raise HTTPException(status_code=404, detail="User not found")

   if not auth_service.verify_password(user.password, record["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

   return {"message": "Login successful"}

@router.post("/analyse_video/")
def analyse_video(video_file: UploadFile):
    # logic to analyze video
    return {"message": "Video analyzed"}

@router.get("/match_history", response_model=list[MatchResponse])
def get_match_history():
    # logic to return match history
    return []

@router.get("/match/{match_name}", response_model=MatchResponse)
def get_match(match_name: str):
    # logic to return specific match
    return {"id": 1, "data": {}, "annotated_video_url": "http://example.com/video.mp4"}
