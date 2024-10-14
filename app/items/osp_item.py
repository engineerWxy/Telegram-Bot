from pydantic import BaseModel, Field


class Osp(BaseModel):
    """
    Osp server 配置
    """
    host: str = Field(..., description="osp host")
    headers: dict = Field(..., description="osp https headers")
