import time
from telegram.error import Forbidden, BadRequest
from telegram import ChatMember, User
from telegram.constants import ChatMemberStatus
from google.protobuf.json_format import MessageToDict

import facade.chat_pb2 as pb2
import facade.chat_pb2_grpc as pb2_grpc
import facade.base_pb2 as base_pb2

from app.core.logger_handler import Log
from app.core.bot_handler import bots
from app.core.grpc_error_decorator import error_handling_decorator
from app.core.error_handler import ValidateParamsError, BotRequestError
from app.utils.enum_util import SaasID, BanType
from app.static.osp import BanChatMemberSendMessage

logger = Log()


class ChatServicer(pb2_grpc.ChatServicer):
    @error_handling_decorator
    async def leaveChat(self, leave_chat_item: pb2.LeaveChatRequest, context):
        logger.info(f"leaveChat: {MessageToDict(leave_chat_item, always_print_fields_with_no_presence=True)}")
        if leave_chat_item.sassId != SaasID.SPACE.value:
            raise ValidateParamsError(f"params error")
        bot = bots["osp_space_group"].bot_client
        try:
            is_leave_chat_success: bool = await bot.leave_chat(leave_chat_item.chatId)
        except BadRequest as e:
            logger.error(f"ban_chat_member bot request failed: {e}")
            raise BotRequestError(str(e))
        if not is_leave_chat_success:
            raise BotRequestError("unknown error: please contact the administrator to view")
        logger.info(f"leave_chat bot request success")
        return base_pb2.CommonResponse(code='0000')
    
    @error_handling_decorator
    async def banChatMember(self, ban_chat_item: pb2.BanChatMemberRequest, context):
        logger.info(f"banChatMember: {MessageToDict(ban_chat_item, always_print_fields_with_no_presence=True)}")
        if ban_chat_item.sassId != SaasID.SPACE.value or ban_chat_item.banType != BanType.Membership.value:
            raise ValidateParamsError(f"params error")
        bot = bots["osp_space_group"].bot_client
        try:
            chat_member: ChatMember = await bot.get_chat_member(ban_chat_item.chatId, ban_chat_item.userId)
            logger.info(f"chat member status: {chat_member.status}")
            if chat_member.status in [ChatMemberStatus.BANNED, ChatMember.LEFT]:
                return
            user_name = self.get_user_name(chat_member.user)
            until_date = int(time.time()) + 35
            is_ban_chat_success: bool = await bot.ban_chat_member(ban_chat_item.chatId, ban_chat_item.userId,
                                                                  until_date=until_date)
        except (Forbidden, BadRequest) as e:
            logger.error(f"ban_chat_member bot request failed: {e}")
            raise BotRequestError(str(e))
        if not is_ban_chat_success:
            raise BotRequestError("unknown error: please contact the administrator to view")
        logger.info(f"ban_chat_member bot request success")
        await bot.send_message(ban_chat_item.chatId,
                               text=BanChatMemberSendMessage.Membership_Expiration.format(user=user_name))
        return base_pb2.CommonResponse(code='0000')
    
    @staticmethod
    def get_user_name(user: User):
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        user_name = f"{first_name} {last_name}"
        return user_name
