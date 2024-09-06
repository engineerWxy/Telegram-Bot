class NewException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(message)


class OSPServerError(NewException):
	pass


class TGUserError(NewException):
	"""用户不被允许进入"""
	pass


class TGTypeError(NewException):
	"""tg type不被允许，比如目前只运训message信息进入"""
	pass


class TGMessageError(NewException):
	"""消息不被允许进入"""
	pass


class TGBotError(NewException):
	"""机器人报错"""
	pass
