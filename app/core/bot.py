import time
from telegram import Bot
from utils.pulse_error import *


class BotServer(object):
	def __init__(self, name, token):
		self.name = name
		self._bot = Bot(token=token)
	
	def get_bot(self):
		return self._bot
	
	async def set_webhook(self, url):
		"""
		设置bot的webhook
		:param url:
		:return:
		"""
		status = await self._bot.set_webhook(url, max_connections=100, drop_pending_updates=True)
		if not status:
			raise TGBotError(f"{self.name} set_webhook error: url={url}")
	
	async def delete_webhook(self):
		status = await self._bot.delete_webhook()
		if not status:
			raise TGBotError(f"{self.name} delete_webhook error")
	
	async def send_message(self, user_id, message, parse_mode=None, user_name=None):
		"""
		发送消息
		:param user_id: 用户ID
		:param message:
		:param parse_mode: 解析格式（html、markdown等）
		:param user_name: 用户的名字first name + last name
		:return:
		"""
		status = await self._bot.send_message(user_id, message, parse_mode)
		if not status:
			raise TGBotError(
				f"{self.name} send_message error: user_id={user_id} user_name={user_name} message={message} parse_mode={parse_mode}")
	
	async def ban_chat_member(self, chat_id, user_id, user_name=None, ban_time=0):
		"""
		限制用户，踢出群聊
		:param chat_id:
		:param user_id:
		:param user_name:
		:param ban_time:
		:return:
		"""
		if ban_time == 0:
			return await self._bot.ban_chat_member(chat_id=chat_id, user_id=user_id, until_date=0)
		until_date = int(time.time()) + ban_time
		status = await self._bot.ban_chat_member(chat_id=chat_id, user_id=user_id, until_date=until_date)
		if not status:
			raise TGBotError(
				f"{self.name} ban_chat_member error: chat_id={chat_id} user_id={user_id} user_name={user_name}")
