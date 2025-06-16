from fastapi import FastAPI
from controller.auth_controller import router as auth_router
from controller.match_controller import router as match_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["UserAPI"])
app.include_router(match_router, prefix="/analysis", tags=["MatchAPI"])