from pydantic import BaseModel
from typing import Optional, Any


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
