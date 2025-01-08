import hashlib
import hmac
import json

from _operator import itemgetter
from urllib.parse import parse_qsl
from fastapi import Header

from app.utils.enum_util import ErrorCodeEnum
from app.core.error_handler import CommonServerError
from app.core.error_handler import DeniedError
from app.config.setting import settings
from app.core.logger_handler import Log

logger = Log()


async def verify_hash(init_data: str = Header(..., description="API verify,data is initDataRaw")) -> dict:
    """
    API verify
    @param init_data: initDataRaw https://core.telegram.org/bots/webapps#initializing-mini-apps
    @return: WebAppUser https://core.telegram.org/bots/webapps#webappuser
    """
    try:
        init_data = dict(parse_qsl(init_data, strict_parsing=True))
        logger.info(f'get initData {init_data}')
    except ValueError:
        logger.error(f'invalid init data,{init_data}')
        raise CommonServerError(ErrorCodeEnum.A001, 'Invalid initDataRaw')
    if not check_init_data(init_data):
        logger.error(f'invalid init data,verify hash fail,{init_data}')
        raise CommonServerError(ErrorCodeEnum.A001, 'Invalid initDataRaw')
    return json.loads(init_data.get('user'))


def check_init_data(init_data):
    """
    1、解析init_data, 从encode 字符串解析成dict
                init_data => user=%7B%22id%22%3A1856146529%2C%22first_name%22%3A%22George%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22george_sic%22%2C%22language_code%22%3A%22zh-hans%22%2C%22allows_write_to_pm%22%3Atrue%7D&chat_instance=2909859642922841330&chat_type=private&auth_date=1724670279&hash=ff688b4fb9ee3807fb6be8b706b3b67e2e8ddaa77f650a8c116a3ab3ef218441
                dict => {'user': '{"id":1856146529,"first_name":"George","last_name":"","username":"george_sic","language_code":"zh-hans","allows_write_to_pm":true}', 'chat_instance': '2909859642922841330', 'chat_type': 'private', 'auth_date': '1724670279', 'hash': 'ff688b4fb9ee3807fb6be8b706b3b67e2e8ddaa77f650a8c116a3ab3ef218441'}
    2、判断hash是否在dict中存在
    3、将dict拼装成校验格式字符串
    4、生成secret key， 使用常量 WebAppData sha256 bot token
    5、使用secret key sha256 校验格式字符串
    6、检查hash 是否和dict中一致

    参考文档：
        https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    @param init_data: initData https://core.telegram.org/bots/webapps#initializing-mini-apps
    @return:
    """
    if "hash" not in init_data:
        return False
    hash_ = init_data.pop("hash")
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(init_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(key=b"WebAppData", msg=settings.ufool_token.encode(), digestmod=hashlib.sha256).digest()
    calculated_hash = hmac.new(key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()
    return hash_ == calculated_hash


async def verify_api_key(api_key: str | None = Header(..., alias="api-key")) -> None:
    if api_key != settings.app.token:
        raise DeniedError(error_msg="request denied")
