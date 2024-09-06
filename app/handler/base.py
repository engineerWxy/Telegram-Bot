from telegram import Update
from fastapi.responses import JSONResponse
from fastapi import Request

from app.core.telegram_message import TGMessage
from app.core.initialize_bots import bots
from utils.log import logger
from utils.pulse_error import *

BLACK_LIST = []


def get_bot_sever(bot_name):
	return getattr(bots, bot_name)


async def get_tg_message(request, bot):
	request_body = await request.json()
	logger.debug(f"request body:{request_body}")
	update = Update.de_json(request_body, bot)
	# 如果user id在黑名单直接退出
	if update.effective_user.id in BLACK_LIST:
		raise TGUserError("user is in blacklist")
	message = update.message or update.edited_message
	# 不是message信息直接退出
	if not message:
		raise TGTypeError("not a message")
	tg_message = TGMessage(message)
	# 不满足message条件直接退出
	if not tg_message.available:
		raise TGMessageError("message rejected")
	return tg_message


async def initialize_server(request, bot_name):
	"""
	获取bot实例 以及 tg message实例
	:param request:
	:param bot_name:
	:return:
	"""
	bot_server = get_bot_sever(bot_name)
	tg_message = await get_tg_message(request, bot_server.get_bot())
	return bot_server, tg_message
