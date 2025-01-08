from typing import Optional, Any
from pydantic import BaseModel
from typing import Dict, List
from app.static.osp import BindSendMessage
from app.utils.enum_util import OspResponseCode
from app.core.logger_handler import Log

logger = Log()


class CommonResponse(BaseModel):
    """
    公共response返回封装
    """
    code: str
    message: str
    error_msg: Optional[Any] = None
    data: Optional[Any] = None


def success_response(data: Any = None, message: str = "Success"):
    """
    response 成功
    :param data:
    :param message:
    :return:
    """
    return CommonResponse(code="0000", message=message, data=data)


def error_response(code: str = "9999", message: str = "msg", error_msg: str = "error_msg"):
    """
    错误的response
    :param code:
    :param message:
    :param error_msg:
    :return:
    """
    return CommonResponse(code=code, error_msg=error_msg, message=message)


class OspResponse(BaseModel):
    code: int
    msg: str | None
    data: Dict | None
    errors: List | None
    
    def get_send_message(self):
        if self.code == OspResponseCode.SUCCESS.value:
            return BindSendMessage.SUCCESS
        elif self.code == OspResponseCode.TG_CONNECTED.value:
            return BindSendMessage.TG_CONNECTED
        elif self.code == OspResponseCode.CODE_EXPIRED.value:
            return BindSendMessage.CODE_EXPIRED
        elif self.code == OspResponseCode.BUSINESS_ERROR.value:
            if isinstance(self.errors, List):
                if detail := self.errors[0].get("detail"):
                    import json
                    detail_dict = json.loads(detail)
                    if detail_dict.get("code") == OspResponseCode.OSP_CONNECTED_ANOTHER_TG.value:
                        return BindSendMessage.OSP_CONNECTED_ANOTHER_TG
        elif self.code == OspResponseCode.SYSTEM_ERROR.value:
            logger.error(
                f"code is {OspResponseCode.SYSTEM_ERROR.value}, msg:{self.msg}, data:{self.data}, errors:{self.errors}")
        return
    
    @property
    def is_success(self):
        return self.code == OspResponseCode.SUCCESS.value
