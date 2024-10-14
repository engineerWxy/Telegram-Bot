import base64
import pickle

import redis

from app.config.setting import settings
from app.utils.object_util import Singleton


class RedisHandler(metaclass=Singleton):
    """
    Redis配置管理
    """
    def __init__(self):
        self.redis = settings.redis
        self._operate = redis.Redis(connection_pool=self.pool)

    @property
    def pool(self):
        """
        初始化Redis配置
        :return:
        """
        return redis.ConnectionPool(host=self.redis.host,
                                    port=self.redis.port,
                                    password=self.redis.password,
                                    max_connections=self.redis.max_total,
                                    db=self.redis.db_index)

    @property
    def op(self):
        return self._operate

    def set_object(self, key, obj):
        serialized_obj = base64.b64encode(pickle.dumps(obj)).decode('utf-8')
        self._operate.set(key, serialized_obj)

    def get_object(self, key):
        serialized_obj = self._operate.get(key)
        if serialized_obj is not None:
            obj = pickle.loads(base64.b64decode(serialized_obj))
            return obj
        return None

    def rpush(self, key, obj):
        serialized_obj = base64.b64encode(pickle.dumps(obj)).decode('utf-8')
        self._operate.rpush(key, serialized_obj)

    def lpop(self, key):
        self._operate.lpop(key)

    def lrange(self, key):
        serialized_obj = self._operate.lrange(key, 0, 0)
        if serialized_obj and serialized_obj[0] is not None:
            obj = pickle.loads(base64.b64decode(serialized_obj[0]))
            return obj
        return None


redis_handler: RedisHandler = RedisHandler()
