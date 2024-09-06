import requests
from config import config
from app.constants import OspApis
from utils.log import logger


class OspApi:
	def __init__(self):
		self.host = config.server.osp.host
		headers = config.server.osp.headers
		self.headers = {
			"OS-App-Id": headers.get("app_id"),
			"OS-Api-Key": headers.get("api_id")
		}
		self.osp_apis = OspApis()
	
	def bind(self, user_id, code, name):
		"""
		osp 玩家绑定telegram
		:param user_id:
		:param code:
		:param name: first name + last name
		:return:
		"""
		data = {
			"platformType": "TELEGRAM",
			"platformUserId": user_id,
			"platformUserName": name,
			"token": code
		}
		logger.debug(f"bind data:{data}")
		url = f"{self.host}/{self.osp_apis.bind}"
		return requests.post(url, json=data, headers=self.headers)
	
	def join_chat_group(self, user_id):
		"""
		审核验证玩家能否进入官方的chat group
		:param user_id:
		:return:
		"""
		data = {
			"platformType": "TELEGRAM",
			"platformUserId": user_id
		}
		logger.debug(f"join_chat_group data:{data}")
		url = f"{self.host}/{self.osp_apis.join_chat_group}"
		return requests.post(url, json=data, headers=self.headers)
