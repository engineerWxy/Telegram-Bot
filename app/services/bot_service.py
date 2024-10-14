import time
from telegram import Update
from telegram.ext import CallbackContext

from app.core.logger_handler import Log
from app.core.osp_apis_handler import OspApis
from app.core.osp_response_handler import OspResponse
from app.core.error_handler import OSPServerError
from app.utils.enum_util import ErrorCodeEnum

logger = Log()


class BotService:
    """
    Bot业务逻辑
    """
    
    def __init__(self, update: Update, context: CallbackContext):
        self.update = update
        self.context = context
        self.osp_apis = OspApis()
    
    async def verify_token(self):
        token = self.context.args[0] if len(self.context.args) == 1 else None
        if not token:
            return
        from_user = self.update.message.from_user
        user_id = from_user.id
        first_name = from_user.first_name if from_user.first_name else ""
        last_name = from_user.last_name if from_user.last_name else ""
        user_name = f"{first_name} {last_name}"
        try:
            response = self.osp_apis.bind(user_id, token, user_name)
            send_message = OspResponse(**response.json()).get_send_message()
        except Exception as e:
            msg = f"osp bind failed:{e}"
            logger.error(msg)
            raise OSPServerError(ErrorCodeEnum.A003, msg)
        else:
            if send_message:
                await self.context.bot.send_message(user_id, send_message)
    
    async def verify_members(self):
        """
        新成员加入的业务逻辑
        :return:
        """
        for chat_member in self.update.message.new_chat_members:  # 处理多个新成员
            user_id = chat_member.id
            try:
                response = self.osp_apis.join_chat_group(user_id)
                logger.debug(response.text)
                osp_res = OspResponse(**response.json())
            except Exception as e:
                msg = f"osp join_chat_group failed:{e}"
                logger.error(f"osp join_chat_group failed:{e}")
                raise OSPServerError(ErrorCodeEnum.A003, msg)
            else:
                if not osp_res.is_success:
                    until_date = int(time.time()) + 60
                    await self.context.bot.ban_chat_member(self.update.message.chat_id, user_id,
                                                           until_date=until_date)