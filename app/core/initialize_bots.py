from app.core.bot import BotServer
from app.constants import BotsRouter
from config import config
from utils.log import logger
from utils.pulse_error import *


class BotsInitialize:
	"""
	初始化多个bot实例
	"""
	_instance = None
	
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls)
			for bot in config.bot:
				name = bot.name
				token = bot.token
				bot_server = BotServer(name, token)
				setattr(cls._instance, name, bot_server)
		return cls._instance


bots = BotsInitialize()


async def bots_set_webhook():
	bots_router = BotsRouter()
	for bot in config.bot:
		name = bot.name
		bot_server = getattr(bots, name)
		if bot_router := getattr(bots_router, name):
			url = f"{config.server.webhook_host}/{bot_router}"
			await bot_server.set_webhook(url)
			logger.info(f"bot:[{name}] url:{url} set webhook success")
