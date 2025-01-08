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
        return self._operate.set(key, serialized_obj)
    
    def get_object(self, key):
        serialized_obj = self._operate.get(key)
        if serialized_obj:
            obj = pickle.loads(base64.b64decode(serialized_obj))
            return obj
    
    def delete_object(self, key):
        return self._operate.delete(key)


redis_handler: RedisHandler = RedisHandler()
