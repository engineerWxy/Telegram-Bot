from app.utils.enum_util import ErrorCodeEnum


class OSPServerError(Exception):
    """
    OSP请求失败
    """
    def __init__(self, error: ErrorCodeEnum, error_msg: str):
        self.code, self.message = error.value
        self.error_msg = error_msg
