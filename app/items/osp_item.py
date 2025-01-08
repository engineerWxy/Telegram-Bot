from pydantic import BaseModel, Field


class Osp(BaseModel):
    """
    Osp server 配置
    """
    domain: str = Field(..., description="osp服务域名")
    headers: dict = Field(..., description="osp https headers")

