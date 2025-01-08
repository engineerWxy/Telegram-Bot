from typing import Literal, Union
from pydantic import BaseModel, Field


class App(BaseModel):
    """
    项目配置
    """
    name: str = Field(..., description="项目名字")
    desc: str = Field(..., description="项目描述")
    domain: Union[str, None] = Field('localhost', description="服务域名")
    env: Literal["prod", "beta", "dev", "pre", "local"] = Field('local', description="环境")
    token: str = Field(..., description="通用接口的token")


class Redis(BaseModel):
    """
    Redis 配置
    """
    host: str = Field(..., description="redis host")
    port: int = Field(..., description="redis port")
    password: str = Field(..., description="redis password")
    db_index: int = Field(..., description="redis db index")
    max_total: int = Field(..., description="redis max total")


class OSS(BaseModel):
    """
    OSS 配置
    """
    bucket: str = Field(..., description="oss bucket")
    access_key_id: str = Field(..., description="oss AccessKeyId")
    access_key_secret: str = Field(..., description="oss AccessKeySecret")
    endpoint: str = Field(..., description="oss endpoint")
