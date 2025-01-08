from fastapi import APIRouter

from app.controller import (
    health_check_controller as health_check_router
)
from app.controller.bot_controller import bot_router
from app.controller.tele_controller import router as tele_router

routers = APIRouter()
routers.include_router(bot_router, prefix="/bot", tags=["bot"])
routers.include_router(health_check_router.health_router, tags=["health check"])
routers.include_router(tele_router, tags=["Tele"])
