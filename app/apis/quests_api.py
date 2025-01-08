import json
import time
import requests
from urllib.parse import urljoin

from app.config.setting import settings
from app.utils.enum_util import SaasID
from app.core.logger_handler import Log

logger = Log()


class QuestsApis:
    
    def __init__(self):
        self.url = f"https://{settings.quests.domain}"
        self.sign = settings.quests.sign
    
    def join_telegram_channel(self, customer_id: str, telegram_id: str):
        """
        join telegram channel
        @param customer_id:
        @param telegram_id:
        @return:
        """
        logger.info(f'start send customer join telegram channel, customer id:{customer_id}, tg id:{telegram_id}')
        params = {
            "name": "join_tg_channel",
            "userId": customer_id,
            "contentId": f"{'join_tg_channel'}_{telegram_id}_{customer_id}_{settings.JOIN_TG_TASK_ID}",
            "eventTime": int(time.time()),
            "extendAttr": json.dumps({"taskId": settings.JOIN_TG_TASK_ID})
        }
        logger.info(f"join telegram channel params:{json.dumps(params)}")
        headers = {"sign": self.sign, "saas_id": SaasID.UFOOL.value}
        url = urljoin(self.url, settings.JOIN_TG_URL)
        logger.info(f"start join telegram channel, url:{url}")
        return requests.post(url, headers=headers, params=params, timeout=30)
        

quests_apis = QuestsApis()
