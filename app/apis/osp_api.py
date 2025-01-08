import requests
from app.config.setting import settings
from app.core.logger_handler import Log

logger = Log()


class OspApis:
    PLATFORM_TYPE = "TELEGRAM"
    
    def __init__(self):
        self.url = f"http://{settings.osp.domain}/v2/s2s"
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
            "platform_type": self.PLATFORM_TYPE,
            "platform_user_id": user_id,
            "platform_user_name": name,
            "token": token
        }
        logger.info(f"bind data:{data}")
        url = f"{self.url}/{settings.BIND}"
        logger.info(f"start call bind, url:{url}")
        return requests.post(url, json=data, headers=self.headers, timeout=30)
    
    def join_chat_group(self, user_id):
        """
        审核验证玩家能否进入官方的chat group
        :param user_id:
        :return:
        """
        data = {
            "platform_type": self.PLATFORM_TYPE,
            "platform_user_id": user_id
        }
        logger.info(f"join chat group data:{data}")
        url = f"{self.url}/{settings.JOIN_CHAT_GROUP}"
        logger.info(f"start call join chat group, url:{url}")
        return requests.post(url, json=data, headers=self.headers, timeout=30)
    
    def chat_group_join_verify(self, user_id, group_id):
        """
        space vip群检验是否有权限加入
        :param user_id:
        :param group_id:
        :return:
        """
        data = {
            "channel": self.PLATFORM_TYPE,
            "group_id": str(group_id),
            "account": str(user_id)
        }
        logger.info(f"chat group join verify data:{data}")
        url = f"{self.url}/{settings.CHAT_GROUP_JOIN_VERIFY}"
        logger.info(f"start call chat group join verify, url:{url}")
        return requests.post(url, json=data, headers=self.headers, timeout=30)
    
    def unbind_chat_group(self, group_id):
        """
        解绑群聊
        :param group_id:
        :return:
        """
        params = {"group_id": str(group_id),
                  "channel": self.PLATFORM_TYPE}
        logger.info(f"unbind chat group params:{params}")
        url = f"{self.url}/{settings.UNBIND}"
        logger.info(f"start call unbind chat group, url:{url}")
        return requests.delete(url, params=params, headers=self.headers)


osp_apis = OspApis()
