class OspApis:
	bind = "platforms/bind"
	join_chat_group = "platforms/join/chat/group"


class BotsRouter:
	personal = "receivePersonalBotMsg"
	group = "receiveGroupBotMsg"


class TGSendMessage:
	SUCCESS = "Telegram connection successful."
	FAILED = "Telegram connection failed."
	OSP_CONNECTED_ANOTHER_TG = "The OSP profile has already connected another Telegram account."
	TG_CONNECTED = "This Telegram account has already been connected."
	CODE_EXPIRED = "This verification code is invalid, Please return to the quest page and click 'Go' again."
