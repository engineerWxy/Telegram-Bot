import requests

from app.core.logger_handler import Log

logger = Log()


class Request:
    """
    封住通用request处理
    """

    def __init__(self, timeout=10):
        self.timeout = timeout

    def request(self, url, method='GET', **kwargs):
        logger.info(f'ready request {url} by params {kwargs}')
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            return response.json()
        except Exception as e:
            logger.error(f'request: {url} exception, error: {e}')
            # raise RequestException(ResponseCode.H001, f'request: {url} exception, error: {e}')


request = Request()
