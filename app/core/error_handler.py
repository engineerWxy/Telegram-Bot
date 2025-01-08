from app.utils.enum_util import ErrorCodeEnum


class CommonServerError(Exception):
    """
    通用错误
    """
    
    def __init__(self, error: ErrorCodeEnum, error_msg: str = ""):
        self.code, self.message = error.value
        self.error_msg = error_msg


class DeniedError(CommonServerError):
    """
    请求拒绝
    """
    
    def __init__(self, error_msg: str = "", error: ErrorCodeEnum = ErrorCodeEnum.A001):
        super().__init__(error, error_msg)


class ValidateParamsError(CommonServerError):
    """
    参数校验异常
    """
    
    def __init__(self, error_msg: str = "", error: ErrorCodeEnum = ErrorCodeEnum.A003):
        super().__init__(error, error_msg)


class BotRequestError(CommonServerError):
    """
    bot请求失败
    """
    
    def __init__(self, error_msg: str = "", error: ErrorCodeEnum = ErrorCodeEnum.T001):
        super().__init__(error, error_msg)


class OSPServerError(CommonServerError):
    """
    osp请求失败
    """
    
    def __init__(self, error_msg: str = "", error: ErrorCodeEnum = ErrorCodeEnum.O001):
        super().__init__(error, error_msg)


class CustomerServerError(CommonServerError):
    """
    customer请求失败
    """
    
    def __init__(self, error_msg: str = "", error: ErrorCodeEnum = ErrorCodeEnum.C001):
        super().__init__(error, error_msg)


class QuestsServerError(CommonServerError):
    """
    quests请求失败
    """
    
    def __init__(self, error_msg: str = "", error: ErrorCodeEnum = ErrorCodeEnum.Q001):
        super().__init__(error, error_msg)


class VerifyGroupLinkError(CommonServerError):
    
    def __init__(self, error_msg: str = "", error: ErrorCodeEnum = ErrorCodeEnum.V001):
        super().__init__(error, error_msg)
