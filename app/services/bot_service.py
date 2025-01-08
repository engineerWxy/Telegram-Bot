import time
import requests
from telegram import Update, ChatMember, ChatMemberUpdated, Bot, User, ChatInviteLink
from telegram.ext import CallbackContext
from typing import Optional, Tuple
from telegram.constants import ChatMemberStatus
from telegram.error import Forbidden, BadRequest

from app.apis.customer_api import customer_apis
from app.apis.quests_api import quests_apis
from app.core.logger_handler import Log
from app.apis.osp_api import osp_apis
from app.items.response_item import OspResponse
from app.core.error_handler import OSPServerError, BotRequestError, CustomerServerError, QuestsServerError, \
    VerifyGroupLinkError
from app.items.telegram_item import ChannelSendRequest, BanChatMemberRequest, LeaveChatRequest, VerifyGroupLinkRequest
from app.items.customer_item import User
from app.static.osp import BanChatMemberSendMessage, JoinDifferentGroupSendMessage
from app.utils.enum_util import GroupType
from app.core.redis_handler import redis_handler

logger = Log()


class BotService:
    """
    Bot python-sdk 业务逻辑
    """
    
    def __init__(self, update: Update = None, context: CallbackContext = None, bot: Bot = None):
        self.update = update
        self.context = context
        self.bot = bot
    
    @staticmethod
    def get_user_name(user: User):
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        user_name = f"{first_name} {last_name}"
        return user_name
    
    async def verify_token(self):
        token = self.context.args[0] if len(self.context.args) == 1 else None
        if not token:
            return
        from_user = self.update.message.from_user
        user_id = from_user.id
        user_name = self.get_user_name(from_user)
        try:
            response = osp_apis.bind(user_id, token, user_name)
            logger.info(f"bind response:{response.text} {response.status_code}")
            send_message = OspResponse(**response.json()).get_send_message()
        except Exception as e:
            msg = f"osp bind failed:{e}"
            logger.error(msg)
            raise OSPServerError(msg)
        else:
            if send_message:
                await self.context.bot.send_message(user_id, send_message)
    
    @staticmethod
    def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:
        """
            Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
            of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
            the status didn't change.
        """
        logger.info('start check member status')
        status_change = chat_member_update.difference().get("status")
        old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))
        if status_change is None:
            return None
        old_status, new_status = status_change
        was_member = old_status in [
            ChatMember.MEMBER,
            ChatMember.OWNER,
            ChatMember.ADMINISTRATOR,
        ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
        is_member = new_status in [
            ChatMember.MEMBER,
            ChatMember.OWNER,
            ChatMember.ADMINISTRATOR,
        ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)
        
        return was_member, is_member
    
    async def greet_chat_members(self):
        result = self.extract_status_change(self.update.chat_member)
        if result is None:
            return
        was_member, is_member = result
        user_id = self.update.chat_member.new_chat_member.user.id
        logger.info(f'new chat member id:{user_id}')
        if not was_member and is_member:
            self.send_join_channel_signal(user_id)
    
    def send_join_channel_signal(self, telegram_id):
        try:
            res = customer_apis.get_customer_id_by_telegram_id(telegram_id)
            logger.info(f"get user info response: {res.text}")
        except Exception as e:
            msg = f"get_customer_id_by_telegram_id failed:{e}"
            logger.error(msg)
            raise CustomerServerError(msg)
        else:
            if res.status_code != 200:
                msg = f"get_customer_id_by_telegram_id fail,status code {res.status_code}, content: {res.text}"
                logger.error(msg)
                raise CustomerServerError(msg)
            data = res.text
            user = User(customer_id=data)
        try:
            res = quests_apis.join_telegram_channel(user.customer_id, str(telegram_id))
            res = res.json()
            logger.info(f"join tg channel response: {res}")
        except Exception as e:
            msg = f'join_telegram_channel customer id:{user.customer_id}, tg id:{telegram_id} failed:{e}'
            logger.error(msg)
            raise QuestsServerError(msg)
        else:
            if res.get("success") and res.get("code") == "0000":
                logger.info(
                    f"send user join channel signal success, customer id:{user.customer_id}, tg id:{telegram_id}")
                return
            else:
                msg = f"join_telegram_channel customer id:{user.customer_id}, tg id:{telegram_id} failed:{res}"
                logger.error(msg)
                raise QuestsServerError(msg)
    
    async def ban_chat_member(self, ban_chat_item: BanChatMemberRequest):
        try:
            chat_member: ChatMember = await self.bot.get_chat_member(ban_chat_item.chat_id, ban_chat_item.user_id)
            logger.info(f"chat member status: {chat_member.status}")
            if chat_member.status in [ChatMemberStatus.BANNED, ChatMember.LEFT]:
                return
            user_name = self.get_user_name(chat_member.user)
            until_date = int(time.time()) + 35
            is_ban_chat_success: bool = await self.bot.ban_chat_member(ban_chat_item.chat_id, ban_chat_item.user_id,
                                                                       until_date=until_date)
        except (Forbidden, BadRequest) as e:
            logger.error(f"ban_chat_member bot request failed: {e}")
            raise BotRequestError(str(e))
        if not is_ban_chat_success:
            raise BotRequestError("unknown error: please contact the administrator to view")
        logger.info(f"ban_chat_member bot request success")
        await self.bot.send_message(ban_chat_item.chat_id,
                                    text=BanChatMemberSendMessage.Membership_Expiration.format(user=user_name))
    
    async def leave_chat(self, leave_chat_item: LeaveChatRequest):
        try:
            is_leave_chat_success: bool = await self.bot.leave_chat(leave_chat_item.chat_id)
        except BadRequest as e:
            logger.error(f"ban_chat_member bot request failed: {e}")
            raise BotRequestError(str(e))
        if not is_leave_chat_success:
            raise BotRequestError("unknown error: please contact the administrator to view")
        logger.info(f"leave_chat bot request success")
    
    async def chat_join_request(self):
        from_user = self.update.chat_join_request.from_user
        if not from_user.is_bot:
            chat = self.update.chat_join_request.chat
            try:
                response = osp_apis.chat_group_join_verify(from_user.id, chat.id)
                logger.info(f"chat group join verify response: {response.text} {response.status_code}")
                osp_res = OspResponse(**response.json())
                if osp_res.is_success and osp_res.data.get("result"):
                    logger.info("can be approve")
                    await self.context.bot.approve_chat_join_request(chat.id, from_user.id)
            except Exception as e:
                msg = f"chat group join verify failed:{e}"
                logger.error(msg)
                raise OSPServerError(msg)
    
    @staticmethod
    def in_group(status):
        return status in [ChatMemberStatus.MEMBER.value, ChatMemberStatus.ADMINISTRATOR.value,
                          ChatMemberStatus.OWNER.value]
    
    @staticmethod
    def not_in_group(status):
        return status in [ChatMemberStatus.BANNED.value, ChatMemberStatus.LEFT.value]
    
    @staticmethod
    def group_permission_downgrade(old_status, new_status):
        """
        admin 权限降级
        :param old_status:
        :param new_status:
        :return:
        """
        if old_status == ChatMemberStatus.ADMINISTRATOR.value:
            return new_status in [ChatMemberStatus.MEMBER.value, ChatMemberStatus.LEFT.value,
                                  ChatMemberStatus.BANNED.value]
        return False
    
    async def on_bot_joined_chat(self, status, chat):
        """
        Bot加入群聊时触发的逻辑
        :param status:当前加入的状态
        :param chat:
        :return:
        """
        # public group has username
        chat_username = chat.username
        logger.info(f"on_bot_joined_chat start, chat_username: [{chat_username}]")
        # 被邀请进公有群会直接退出
        if chat_username:
            await self.context.bot.send_message(chat_id=chat.id,
                                                text=JoinDifferentGroupSendMessage.Join_Public_Group)
            await self.context.bot.leave_chat(chat.id)
            return
        # 被设置为管理员后才会触发
        if status == ChatMemberStatus.ADMINISTRATOR.value:
            logger.info(f"set invite link start")
            chat_link_obj: ChatInviteLink = await self.context.bot.create_chat_invite_link(chat_id=chat.id,
                                                                                           creates_join_request=True,
                                                                                           expire_date=None)
            invite_link = chat_link_obj.invite_link
            await self.context.bot.send_message(chat_id=chat.id,
                                                text=JoinDifferentGroupSendMessage.Join_Private_Group.format(
                                                    invite_link=invite_link))
            redis_data = {"title": chat.title, "group_id": chat.id, "type": GroupType.Private.value,
                          "created": int(time.time()), "invite_link": invite_link}
            logger.info(f"redis_data: {redis_data}")
            redis_handler.set_object(invite_link, redis_data)
    
    async def chat_member_change(self):
        """
        bot chat status change
        :return:
        """
        chat_member_updated: ChatMemberUpdated = self.update.my_chat_member
        status_change = chat_member_updated.difference().get("status")
        if status_change:
            old_status, new_status = status_change
            logger.info(f"old status: [{old_status}], new status: [{new_status}]")
            chat = chat_member_updated.chat
            # 不在群聊 -> 加入群聊
            if (self.not_in_group(old_status) and self.in_group(new_status)) or (
                # 群聊普通人员 -> 群聊管理员
                old_status == ChatMemberStatus.MEMBER.value and new_status == ChatMemberStatus.ADMINISTRATOR.value):
                await self.on_bot_joined_chat(new_status, chat)
            # admin -> 被踢出或者降级为普通人员
            elif self.group_permission_downgrade(old_status, new_status):
                try:
                    response = osp_apis.unbind_chat_group(chat.id)
                    logger.info(f"unbind chat group response:{response.text} {response.status_code}")
                except Exception as e:
                    msg = f"unbind chat group failed:{e}"
                    logger.error(msg)
                    raise OSPServerError(msg)


class BotRequestService:
    """
    Bot http 业务逻辑
    """
    
    def __init__(self, bot_token):
        self.token = bot_token
        self.url = f"https://api.telegram.org/bot{self.token}"
    
    def pin_chat_message(self, chat_id, message_id):
        url = f"{self.url}/pinChatMessage"
        data = {
            "message_id": message_id,
            "chat_id": chat_id
        }
        logger.info(f"pin_chat_message url: {url}, data: {data}")
        response = requests.post(url, json=data, timeout=30)
        if response.status_code != 200:
            raise BotRequestError(f"tg api call [pinChatMessage] failed, reason:{response.json()}")
    
    def channel_send(self, channel_item: ChannelSendRequest):
        
        data = {
            "chat_id": channel_item.channel_name,
            "reply_markup": {"inline_keyboard": channel_item.inline_keyboard}
        }
        if photo := channel_item.photo:
            data["caption"] = channel_item.message
            data["photo"] = photo
            method = "sendPhoto"
        else:
            data["text"] = channel_item.message
            method = "sendMessage"
        url = f"{self.url}/{method}"
        logger.info(f"channel_send url: {url}, data: {data}")
        response = requests.post(url, json=data, timeout=30)
        if response.status_code != 200:
            raise BotRequestError(f"tg api call [{method}] failed, reason:{response.json()}")
        if message_id := response.json().get("result", dict()).get("message_id"):
            self.pin_chat_message(channel_item.channel_name, message_id)
        else:
            raise BotRequestError(f"tg api call [{method}] failed, reason:{response.json()}")


class CommonService:
    """不涉及到bot的业务"""
    
    @staticmethod
    def verify_group_link(verify_group_link_item: VerifyGroupLinkRequest):
        group_link = verify_group_link_item.group_link
        if verify_group_link_item.group_type == GroupType.Private.value:
            group_data = redis_handler.get_object(group_link)
            logger.info(f"redis group data:{group_data}")
            if group_data:
                if not redis_handler.delete_object(group_link):
                    logger.error("redis delete:{verify_group_link_item.group_link} failed, please check")
                return group_data
            raise VerifyGroupLinkError(error_msg="no tg link information")
        else:
            try:
                group_link_name = group_link.split("t.me/")[-1]
                res = requests.get(verify_group_link_item.group_link, timeout=30)
                if res.status_code == 200 and ("View in Telegram" in res.text or "Join Group" in res.text):
                    group_data = {
                        "title": group_link_name, "group_id": group_link_name, "type": GroupType.Public.value,
                        "invite_link": group_link, "created": int(time.time())
                    }
                    return group_data
                msg = f"tg link does not exist: {group_link}"
                logger.error(msg)
                raise VerifyGroupLinkError(msg)
            except VerifyGroupLinkError:
                raise
            except Exception as e:
                logger.error(str(e))
                raise VerifyGroupLinkError(error_msg="tg link is invalid")
