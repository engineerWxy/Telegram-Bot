import requests
from urllib.parse import urljoin

from app.config.setting import settings
from app.core.logger_handler import Log

logger = Log()


class CustomerApis(object):
    def __init__(self):
        self.url = f"http://{settings.customer.domain}"
    
    def get_customer_id_by_telegram_id(self, telegram_id: str):
        """
        通过telegram id 获取 user id
        @param telegram_id:
        @return:
        """
        url = urljoin(self.url, settings.OPEN_AUTH.format(telegram_id))
        logger.info(f"start call open auth, url:{url}")
        return requests.get(url, timeout=30)


customer_apis = CustomerApis()
