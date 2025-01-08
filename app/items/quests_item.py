from pydantic import BaseModel, Field, AliasChoices


class Quests(BaseModel):
    domain: str = Field(..., description="任务服务域名")
    sign: str = Field(..., description="任务系统签名")


class QuestsJoinChannelResponse(BaseModel):
    code: str = Field(..., description="业务code码", title='success')
    success: bool = Field(..., description="接口调用是否成功", title='success')
    msg: str = Field(..., description="接口返回信息",
                     validation_alias=AliasChoices('msgKey', 'message', 'msg'))
