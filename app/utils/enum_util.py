from enum import Enum, unique


@unique
class ErrorCodeEnum(Enum):
    """
    通用Response Code码和含义
    """
    A001 = ("1001", "Authentication Error")
    A002 = ("1002", "PermissionDenied Error")
    A003 = ("1003", "Osp Error")


@unique
class OspResponseCode(Enum):
    SUCCESS = 0
    TG_CONNECTED = 10000
    CODE_EXPIRED = 11304
    BUSINESS_ERROR = 14000
    OSP_CONNECTED_ANOTHER_TG = 200006
