from pydantic import BaseModel, Field


class UFool(BaseModel):
    """
    UFool配置
    """
    mini_app_url: str = Field(..., description="tg mini app url")
    ann_url: str = Field(..., description="tg channel url")
