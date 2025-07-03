from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from controller.auth_controller import router as auth_router
from controller.match_controller import router as match_router
from controller.analysis_controller import router as analysis_router
from controller.notification_controller import router as notification_router
from fastapi.middleware.cors import CORSMiddleware
from utils.exceptions import validation_exception_handler

origins = [
    "*",
]
app = FastAPI()

# Register exception handlers
app.exception_handler(RequestValidationError)(validation_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth", tags=["UserAPI"])
app.include_router(match_router, prefix="/match", tags=["MatchAPI"])
app.include_router(notification_router, prefix="/notifications", tags=["NotificationAPI"])
app.include_router(analysis_router, prefix="/analysis", tags=["AnalysisAPI"])
