import yaml
from typing import List, Dict
from pydantic import BaseModel


class OSPInfo(BaseModel):
	host: str
	headers: Dict


class ServerInfo(BaseModel):
	osp: OSPInfo
	webhook_host: str


class BotInfo(BaseModel):
	name: str
	token: str


class ConfigInfo(BaseModel):
	server: ServerInfo
	bot: List[BotInfo]


class ConfigSingleton:
	_instance = None
	
	def __new__(cls):
		if cls._instance is None:
			with open('static/config_demo.yaml') as f:
				content = yaml.safe_load(f.read())
			# 创建 ConfigInfo 的实例，并传递解析的配置数据
			cls._instance = ConfigInfo(**content)
		return cls._instance


config = ConfigSingleton()
