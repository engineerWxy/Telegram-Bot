from typing import Literal, Union
from pydantic import BaseModel, Field


class App(BaseModel):
    """
    项目配置
    """
    name: str = Field(..., description="项目名字")
    desc: str = Field(..., description="项目描述")
    domain: Union[str, None] = Field('localhost', description="app服务地址")
    env: Literal["prod", "beta", "dev", "pre", "local"] = Field('local', description="环境")


class Redis(BaseModel):
    """
    Redis 配置
    """
    host: str = Field(..., description="redis host")
    port: str = Field(..., description="redis port")
    password: str = Field(..., description="redis password")
    db_index: int = Field(..., description="redis db index")
    max_total: int = Field(..., description="redis max total")
