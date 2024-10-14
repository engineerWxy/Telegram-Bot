import requests
from app.config.setting import settings
from app.core.logger_handler import Log

logger = Log()


class OspApis:
    def __init__(self):
        self.host = settings.osp.host
        headers = settings.osp.headers
        self.headers = {
            "OS-App-Id": headers.get("app_id"),
            "OS-Api-Key": headers.get("api_key")
        }
    
    def bind(self, user_id, token, name):
        """
        osp 玩家绑定telegram
        :param user_id:
        :param token:
        :param name: first name + last name
        :return:
        """
        data = {
            "platform_type": "TELEGRAM",
            "platform_user_id": user_id,
            "platform_user_name": name,
            "token": token
        }
        logger.info(f"bind data:{data}")
        url = f"{self.host}/{settings.bind}"
        logger.info(url)
        return requests.post(url, json=data, headers=self.headers)
    
    def join_chat_group(self, user_id):
        """
        审核验证玩家能否进入官方的chat group
        :param user_id:
        :return:
        """
        data = {
            "platform_type": "TELEGRAM",
            "platform_user_id": user_id
        }
        logger.debug(f"join_chat_group data:{data}")
        url = f"{self.host}/{settings.join_chat_group}"
        return requests.post(url, json=data, headers=self.headers)
