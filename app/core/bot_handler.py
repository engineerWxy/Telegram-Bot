from pydantic import computed_field
from telegram.ext import Application

from app.config.setting import settings
from app.core.logger_handler import Log

logger = Log()


class TelegramBot:
    """
    封装Tg bot 相关接口和方法
    """
    
    def __init__(self, name, token):
        self.bot_name = name
        self.bot_app = Application.builder().token(token).build()
        self.bot_client = self.bot_app.bot
    
    async def start_event(self):
        """
        启动初始化上下文
        :return:
        """
        await self.bot_app.initialize()
        await self.start_webhook()
    
    async def shutdown_event(self):
        """
        服务关闭
        :return:
        """
        await self.bot_app.bot.delete_webhook()
        await self.bot_app.shutdown()
    
    async def start_webhook(self) -> bool:
        """
        设置webhook
        :return: 是否设置成功
        """
        is_webhook = await self.bot_client.set_webhook(self.set_webhook_url)
        logger.info(f"set webhook status: {is_webhook}, url: {self.set_webhook_url}")
        return True if is_webhook else False
    
    @computed_field  # type: ignore[prop-decorator]
    @property
    def set_webhook_url(self) -> str:
        """
        构建set_webhook 回调路径
        :return:
        """
        webhook_key = f'{self.bot_name}_webhook'.upper()
        return f"https://{settings.app.domain}{getattr(settings, webhook_key)}"


bots = dict()
for project, project_obj in settings.bot.__dict__.items():
    for sub_project, sub_project_obj in project_obj.__dict__.items():
        for bot in sub_project_obj:
            bot_name = f"{project}_{sub_project}_{bot.name}"
            bots[bot_name] = TelegramBot(bot_name, bot.token)
