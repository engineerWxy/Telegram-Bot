from pydantic import BaseModel, Field


class Bot(BaseModel):
    """
    telegram bot 配置
    """
    name: str = Field(..., description="bot name")
    token: str = Field(..., description="bot token")
