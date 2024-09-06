from fastapi import Request, APIRouter

from utils.log import logger
from app.handler.base import initialize_server
from app.core.osp_api import OspApi
from app.core.telegram_message import TGChatType
from app.core.osp_response_management import OspResponseManagement

router = APIRouter()


@router.post('/receivePersonalBotMsg')
async def personal_webhook(request: Request):
	"""
	:param request:
	:return:
	"""
	bot_server, tg_message = await initialize_server(request, "personal")
	if TGChatType.is_private(tg_message.chat_type):
		logger.debug(f"token:{tg_message.code}")
		response = OspApi().bind(tg_message.user_id, tg_message.code, tg_message.user_id)
		logger.debug(response.json())
		send_message = OspResponseManagement(**response.json()).get_send_message()
		await bot_server.send_message(tg_message.from_user.id, send_message)


@router.post('/receiveGroupBotMsg')
async def group_webhook(request: Request):
	"""
	:param request:
	:return:
	"""
	bot_server, tg_message = await initialize_server(request, "group")
	if TGChatType.is_group(tg_message.chat_type):
		logger.debug(f"new_chat_members:{tg_message.new_chat_members}")
		await verify_new_chat_members(bot_server, tg_message)


async def verify_new_chat_members(bot_server, tg_message):
	osp_api = OspApi()
	for new_chat_member in tg_message.new_chat_members:
		user_id = new_chat_member.id
		user_name = new_chat_member.name
		# is_bot = new_chat_member.is_bot
		# if is_bot:
		# 	status = await bot_server.ban_chat_member(tg_message.chat_id, user_id, ban_time=40)
		# 	continue
		response = osp_api.join_chat_group(user_id)
		if not OspResponseManagement(**response.json()).is_success:
			await bot_server.ban_chat_member(tg_message.chat_id, user_id, user_name=user_name, ban_time=60)
