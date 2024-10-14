from fastapi import APIRouter

from app.controller import (
    health_check_controller as health_check_router
)
from app.controller import bot_controller as bot_router

routers = APIRouter()
routers.include_router(bot_router.person_bot_router, prefix="/bot", tags=["bot"])
routers.include_router(health_check_router.health_router, tags=["health check"])

