import telegram


class TGChatType:
	private = "private"
	group = "group"
	supergroup = "supergroup"
	
	@classmethod
	def is_group(cls, chat_type):
		return chat_type in [cls.group, cls.supergroup]
	
	@classmethod
	def is_private(cls, chat_type):
		return chat_type == cls.private


class TGMessage:
	def __init__(self, message, order="/start"):
		self.message = message
		self.order = order
		self._initialize()
	
	def _initialize(self):
		self.available = False
		try:
			self.chat = self.message.chat
			self.from_user = self.message.from_user
			if TGChatType.is_private(self.chat_type):
				if not self.is_bot and self.text.strip().startswith(self.order):
					if self.code:
						self.available = True
			elif TGChatType.is_group(self.chat_type):
				if self.new_chat_members:
					self.available = True
		except telegram.error.ChatMigrated:
			pass
	
	@property
	def chat_type(self):
		return str(self.chat.type)
	
	@property
	def chat_id(self):
		return self.chat.id
	
	@property
	def user_id(self):
		return self.from_user.id
	
	@property
	def name(self):
		first_name = self.from_user.first_name if self.from_user.first_name else ""
		last_name = self.from_user.last_name if self.from_user.last_name else ""
		return f"{first_name} {last_name}"
	
	@property
	def text(self):
		return self.message.text if self.message.text else ""
	
	@property
	def is_bot(self):
		return self.from_user.is_bot
	
	@property
	def code(self):
		return self.text.replace(self.order, "").strip()
	
	@property
	def new_chat_members(self):
		return self.message.new_chat_members
