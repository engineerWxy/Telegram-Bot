from pydantic import BaseModel, Field
from typing import List


class Bot(BaseModel):
    """
    telegram bot 配置
    """
    name: str = Field(..., description="bot name")
    token: str = Field(..., description="bot token")


class OSPBots(BaseModel):
    common: List[Bot]
    space: List[Bot]


class UFOolBots(BaseModel):
    common: List[Bot]


class Bots(BaseModel):
    osp: OSPBots
    ufool: UFOolBots
