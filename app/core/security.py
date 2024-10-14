import hashlib
import hmac
from operator import itemgetter
from urllib.parse import quote

from app.config.setting import settings

"""
security 是用于由tg bot进行注册用户进行的验证方式
"""


def calculated_hash(data_check_string: str) -> str:
    """
    计算hash
    :return:
    """
    secret_key = hmac.new(key=b"WebAppData", msg=settings.bot.api_token.encode(), digestmod=hashlib.sha256).digest()
    return hmac.new(key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()


def build_data_check_string(user: dict) -> str:
    """
    获取data check 字符串
    :param user:
    :return:
    """
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(user.items(), key=itemgetter(0))
    )
    return data_check_string


def build_id_token(user: dict) -> str:
    """
    根据当前用户封装后的数据 获取 kcustomer签名id token
    :param user:
    :return:
    """
    id_token = "&".join(
        f"{k}={quote(str(v))}" for k, v in sorted(user.items(), key=itemgetter(0))
    )
    return id_token
