from fastapi import APIRouter

from app.items.response_item import success_response

health_router = APIRouter()


@health_router.get("/")
async def health_check():
    """
    项目启动健康检查
    """
    return success_response()
