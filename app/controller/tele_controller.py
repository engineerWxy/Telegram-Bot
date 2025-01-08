from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.core.error_handler import BotRequestError, ValidateParamsError
from app.core.logger_handler import Log
from app.utils.enum_util import OspVerifyEnum
from app.items.telegram_item import StarsPayRequest, StarsPayItem, StarsPayResponse, VerifyResponse, VerifyItem
from app.items.response_item import success_response
from app.core.verify_header import verify_hash
from app.core.bot_handler import bots

router = APIRouter()
logger = Log()


@router.post("/payLink", response_model=StarsPayResponse)
async def pay_link(item: StarsPayRequest, user_info: str = Depends(verify_hash)):
    """
    stars pay link
    :param item:
    :param user_info: https://core.telegram.org/bots/webapps#webappuser
    :return:
    """
    logger.info(f'ready create pay link {item.title} {item.amount} for user {user_info}')
    bot = bots['ufool_common_ufool_pay']
    try:
        link = await bot.bot_client.create_invoice_link(
            item.title, item.description, '{}', '', 'XTR', [{"label": item.label, "amount": item.amount}],
            photo_url=item.image or ''
        )
    except Exception as e:
        logger.error(f'Telegram bot execute create_invoice_link error {e}')
        raise BotRequestError(f'create_invoice_link error {e}')
    logger.info(f'Telegram createInvoiceLink {link}')
    data = StarsPayItem(link=link)
    return success_response(data=data)


@router.get('/teleVerify', response_model=VerifyResponse)
async def verify_info(verify: OspVerifyEnum,
                      chat_name: str = Query(None, description="Chat name"),
                      user_info=Depends(verify_hash)
                      ):
    """
    OSP Telegram Verification
    :param verify:
    :param chat_name:
    :param user_info:
    :return:
    """
    logger.info(f'ready verify {verify.value} for user {user_info}')
    user_id = user_info['id']
    data = VerifyItem()
    is_premium = user_info.get('is_premium')
    if isinstance(is_premium, bool):
        data.is_premium = is_premium
    if verify == OspVerifyEnum.UserPremium:
        return success_response(data=data)
    if not chat_name:
        raise ValidateParamsError('Param chat_name is empty')
    bot = bots['ufool_common_ufool']
    try:
        result = await bot.bot_client.get_user_chat_boosts(chat_name, user_id)
    except Exception as e:
        logger.error(f'Telegram bot execute get_user_chat_boosts error {e}')
        raise BotRequestError(f'get_user_chat_boosts error {e}')
    logger.info(f'bot get user chat boost {result.boosts}')
    data.is_boost = bool(result.boosts)
    for boost in result.boosts:
        if boost.source.user.id == user_id and boost.expiration_date.timestamp() < datetime.now().timestamp():
            data.is_boost = False
            break
    return success_response(data=data)
