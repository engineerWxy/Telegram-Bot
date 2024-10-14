from contextlib import asynccontextmanager
from fastapi import FastAPI
from telegram.ext import CommandHandler, filters, MessageHandler

from app.controller.bot_controller import personal_start, group_new_member
from app.core.bot_handler import bots
from app.core.logger_handler import Log

logger = Log()


@asynccontextmanager
async def context(app: FastAPI):
    """
    项目启动时预加载信息
    :param app:
    :return:
    """
    logger.info("ready start app, init msg...")
    for bot in bots.values():
        await bot.start_event()
        command_management(bot)
    logger.info("init msg finish, start app...")
    yield
    logger.warning("stop app ing...")
    for bot in bots.values():
        await bot.shutdown_event()
    logger.warning("tg bot showdown")


def command_management(bot):
    """
    项目中命令管理
    :return:
    """
    if bot.bot_name == "personal":
        bot.bot_app.add_handler(CommandHandler("start", personal_start))
    elif bot.bot_name == "group":
        bot.bot_app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, group_new_member))
