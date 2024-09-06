from pydantic import BaseModel
from typing import Dict, List
from app.constants import TGSendMessage


class ResponseCode:
	SUCCESS = 0
	TG_CONNECTED = 10000
	CODE_EXPIRED = 11304
	BUSINESS_ERROR = 14000
	OSP_CONNECTED_ANOTHER_TG = 200006


class OspResponseManagement(BaseModel):
	code: int
	msg: str
	data: Dict|None
	errors: List
	
	def get_send_message(self):
		if self.code == ResponseCode.SUCCESS:
			return TGSendMessage.SUCCESS
		elif self.code == ResponseCode.TG_CONNECTED:
			return TGSendMessage.TG_CONNECTED
		elif self.code == ResponseCode.CODE_EXPIRED:
			return TGSendMessage.CODE_EXPIRED
		elif self.code == ResponseCode.BUSINESS_ERROR:
			if detail := self.errors[0].get("detail"):
				import json
				detail_dict = json.loads(detail)
				if detail_dict.get("code") == ResponseCode.OSP_CONNECTED_ANOTHER_TG:
					return TGSendMessage.OSP_CONNECTED_ANOTHER_TG
		return ""
	
	@property
	def is_success(self):
		return self.code == ResponseCode.SUCCESS
