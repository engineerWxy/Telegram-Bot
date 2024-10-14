from fastapi import APIRouter, Request
from telegram import Update
from telegram.ext import CallbackContext

from app.core.bot_handler import bots
from app.core.logger_handler import Log
from app.items.response_item import success_response
from app.services.bot_service import BotService

person_bot_router = APIRouter()
logger = Log()


@person_bot_router.post("/receivePersonalBotMsg")
async def receive_personal_bot(request: Request):
    """
    设置webhook接收个人机器人消息
    :param request:
    :return:
    """
    data = await request.json()
    logger.info(f"receive message: {data}")
    bot = bots["personal"]
    update = Update.de_json(data, bot.bot_app.bot)
    # 处理更新
    res = await bot.bot_app.process_update(update)
    return success_response(data=res)


async def personal_start(update: Update, context: CallbackContext):
    """
     /start 命令入口
    :param update:
    :param context:
    :return:
    """
    logger.info(f"start: context: {context}, args: {context.args}")
    if update.message.chat.type != "private":
        return
    res = await BotService(update, context).verify_token()
    return res


@person_bot_router.post("/receiveGroupBotMsg")
async def receive_group_bot(request: Request):
    """
    设置webhook接收群聊机器人消息
    :param request:
    :return:
    """
    data = await request.json()
    logger.info(f"receive message: {data}")
    bot = bots["group"]
    update = Update.de_json(data, bot.bot_app.bot)
    # 处理更新
    res = await bot.bot_app.process_update(update)
    return success_response(data=res)


async def group_new_member(update: Update, context: CallbackContext):
    """新成员加入"""
    logger.info(f"new_member::::: {update.to_json()}")
    if update.message.chat.type not in ["group", "supergroup"]:
        return
    res = await BotService(update, context).verify_members()
    return res
