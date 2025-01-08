import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import List
from telegram.ext import CommandHandler, ChatMemberHandler, ChatJoinRequestHandler
from app.controller.bot_controller import osp_common_personal_start, ufool_common_ufool_start, greet_chat_members, \
    error_handler, chat_join_request, chat_member_change
from app.core.bot_handler import bots
from app.core.logger_handler import Log
from app.init.init_grpc import start_grpc_server, stop_grpc_server

logger = Log()

handlers = {
    "osp_common_personal": CommandHandler("start", osp_common_personal_start),
    "osp_space_group": [ChatJoinRequestHandler(chat_join_request), ChatMemberHandler(chat_member_change)],
    "ufool_common_ufool": [CommandHandler("start", ufool_common_ufool_start),
                           ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER)]
}


@asynccontextmanager
async def context(app: FastAPI):
    """
    项目启动时预加载信息
    :param app:
    :return:
    """
    logger.info("ready start app, init msg...")
    # bot注册
    for bot, bot_obj in bots.items():
        if bot_obj.bot_client.token == bots["ufool_common_ufool_pay"].bot_client.token:
            continue
        await bot_obj.start_event()
        command_management(bot_obj)
        
    # grpc启动，后台启动
    loop = asyncio.get_running_loop()
    loop.create_task(start_grpc_server())
    logger.info("init msg finish, start app...")
    yield
    logger.warning("stop app ing...")
    # bot下线
    for bot, bot_obj in bots.items():
        await bot_obj.shutdown_event()
    logger.warning("tg bot showdown")
    
    # grpc服务 stop
    await stop_grpc_server()


def command_management(bot):
    """
    项目中命令管理
    :return:
    """
    if handler := handlers.get(bot.bot_name):
        if isinstance(handler, List):
            bot.bot_app.add_handlers(handler)
        else:
            bot.bot_app.add_handler(handler)
        bot.bot_app.add_error_handler(error_handler)
