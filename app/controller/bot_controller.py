from fastapi import APIRouter, Request, Depends
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from telegram.constants import ChatType

from app.core.bot_handler import bots
from app.core.logger_handler import Log
from app.items.response_item import success_response
from app.items.telegram_item import ChannelSendRequest, BanChatMemberRequest, LeaveChatRequest, VerifyGroupLinkRequest
from app.services.bot_service import BotService, BotRequestService, CommonService
from app.core.verify_header import verify_api_key
from app.static.ufool import WELCOME_STYLE
from app.config.setting import settings
from app.utils.enum_util import SaasID, BanType, GroupType
from app.core.error_handler import ValidateParamsError

bot_router = APIRouter()
logger = Log()


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(f"error_handler:{context.error}")


@bot_router.post("/receiveOspCommonPersonalBotMsg", include_in_schema=False)
async def receive_osp_common_personal_bot(request: Request):
    """
    osp绑定机器人
    :param request:
    :return:
    """
    data = await request.json()
    logger.info(f"osp_common_personal receive message: {data}")
    bot = bots["osp_common_personal"]
    update = Update.de_json(data, bot.bot_app.bot)
    # 处理更新
    await bot.bot_app.process_update(update)
    return success_response()


async def osp_common_personal_start(update: Update, context: CallbackContext):
    """
     /start 命令入口
    :param update:
    :param context:
    :return:
    """
    logger.info(f"start: context: {context}, args: {context.args}")
    if update.message.chat.type != ChatType.PRIVATE.value:
        return
    await BotService(update, context).verify_token()


@bot_router.post("/receiveOspSpaceGroupBotMsg", include_in_schema=False)
async def receive_osp_space_group_bot(request: Request):
    """
    space群聊机器人
    :param request:
    :return:
    """
    data = await request.json()
    logger.info(f"osp_space_group receive message: {data}")
    bot = bots["osp_space_group"]
    update = Update.de_json(data, bot.bot_app.bot)
    # 处理更新
    await bot.bot_app.process_update(update)
    return success_response()


async def chat_member_change(update: Update, context: CallbackContext):
    """
    监听bot 在群组的信息变化
    :param update:
    :param context:
    :return:
    """
    if update.my_chat_member.chat.type not in [ChatType.GROUP.value, ChatType.SUPERGROUP.value]:
        return
    await BotService(update, context).chat_member_change()


async def chat_join_request(update: Update, context: CallbackContext):
    """
    监听加群信息
    :param update:
    :param context:
    :return:
    """
    if update.chat_join_request.chat.type not in [ChatType.GROUP.value, ChatType.SUPERGROUP.value]:
        return
    await BotService(update, context).chat_join_request()


@bot_router.post("/receiveUFoolCommonUFoolBotMsg", include_in_schema=False)
async def receive_ufool_common_ufool_bot(request: Request):
    """
    ufool机器人
    :param request:
    :return:
    """
    data = await request.json()
    logger.info(f"ufool_common_ufool receive message: {data}")
    bot = bots["ufool_common_ufool"]
    update = Update.de_json(data, bot.bot_app.bot)
    # 处理更新
    await bot.bot_app.process_update(update)
    return success_response()


async def ufool_common_ufool_start(update: Update, context: CallbackContext):
    """
     /start 命令入口
    :param update:
    :param context:
    :return:
    """
    logger.info(f"start: context: {context}, args: {context.args}")
    if update.message.chat.type != ChatType.PRIVATE.value:
        return
    text = WELCOME_STYLE["text"]
    keyboard = WELCOME_STYLE.get('keyboard') or [],
    photo = f"http://{settings.oss.bucket}.{settings.oss.endpoint}.aliyuncs.com/{settings.UFOOL_WELCOME_IMAGE}"
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=text, reply_markup=keyboard[0])


async def greet_chat_members(update: Update, context: CallbackContext):
    """
     Greets new users in chats and announces when someone leaves
    :param update:
    :param context:
    :return:
    """
    await BotService(update, context).greet_chat_members()


@bot_router.post("/channel")
async def send_to_channel(channel_item: ChannelSendRequest, _api_key: str = Depends(verify_api_key)):
    """
    通用channel接口
    :param channel_item:
    :param _api_key:
    :return:
    """
    if channel_item.sass_id == SaasID.UFOOL.value:
        bot = bots["ufool_common_ufool"]
        bot_token = bot.bot_client.token
        BotRequestService(bot_token).channel_send(channel_item)
    return success_response()


@bot_router.post("/ban/chat/member")
async def ban_chat_member(ban_chat_item: BanChatMemberRequest, _api_key: str = Depends(verify_api_key)):
    """
    通用chat ban人接口
    :param ban_chat_item:
    :param _api_key:
    :return:
    """
    logger.info(f"ban_chat_item:{ban_chat_item.__dict__}")
    if ban_chat_item.sass_id == SaasID.SPACE.value and ban_chat_item.ban_type == BanType.Membership.value:
        bot = bots["osp_space_group"]
        await BotService(bot=bot.bot_client).ban_chat_member(ban_chat_item)
    else:
        raise ValidateParamsError(f"params error")
    return success_response()


@bot_router.post("/leave/chat")
async def leave_chat(leave_chat_item: LeaveChatRequest, _api_key: str = Depends(verify_api_key)):
    """
    通用离开chat接口
    :param leave_chat_item:
    :param _api_key:
    :return:
    """
    logger.info(f"leave_chat_item:{leave_chat_item.__dict__}")
    if leave_chat_item.sass_id == SaasID.SPACE.value:
        bot = bots["osp_space_group"]
        await BotService(bot=bot.bot_client).leave_chat(leave_chat_item)
    else:
        raise ValidateParamsError(f"params error")
    return success_response()


@bot_router.post("/verify/group/link")
async def verify_group_link(verify_group_link_item: VerifyGroupLinkRequest, _api_key: str = Depends(verify_api_key)):
    """
    通用检查 群聊邀请链接 接口
    :param verify_group_link_item:
    :param _api_key:
    :return:
    """
    logger.info(f"verify_group_link_item:{verify_group_link_item.__dict__}")
    if verify_group_link_item.group_type not in (group_type.value for group_type in GroupType):
        raise ValidateParamsError(f"params error")
    group_data = CommonService().verify_group_link(verify_group_link_item)
    return success_response(data=group_data)
