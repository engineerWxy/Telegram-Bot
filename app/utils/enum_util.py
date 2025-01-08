from enum import Enum, unique


@unique
class ErrorCodeEnum(Enum):
    """
    通用Response Code码和含义
    """
    A001 = ("1001", "Authentication Error")
    A002 = ("1002", "Authentication Expired")
    A003 = ("1003", "Input Exception")
    T001 = ("2001", "Telegram API Error")
    O001 = ("3001", "OSP Server Error")
    C001 = ("4001", "Customer API Error")
    Q001 = ("5001", "Quests Server Error")
    V001 = ("6001", "Verify Error")


@unique
class OspResponseCode(Enum):
    SUCCESS = 0
    TG_CONNECTED = 10000
    CODE_EXPIRED = 11304
    BUSINESS_ERROR = 14000
    OSP_CONNECTED_ANOTHER_TG = 200006
    SYSTEM_ERROR = 14003


@unique
class SaasID(Enum):
    UFOOL = "ufool"
    OSP = "osp"
    SPACE = "space"


class OspVerifyEnum(Enum):
    """
    Osp Telegram verification enum
    """
    ChatBoost = 'boost'
    UserPremium = 'premium'


class BanType(Enum):
    """
    Why ban people?
    Membership：Membership Expiration
    """
    Membership = 0
    Tribe = 1


class GroupType(Enum):
    """
    osp group type, not tg group type，
    Private is paid,
    Public is free
    """
    Private = 0
    Public = 1
