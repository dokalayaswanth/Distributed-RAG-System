from fastapi import APIRouter
from app.config import settings

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

@router.get("/")
async def health():
    return {
        "status": "ok",
        "api": "running",
        "environment": settings.app_env
    }