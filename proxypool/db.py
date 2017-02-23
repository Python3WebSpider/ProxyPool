import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import HOST, PORT


class RedisClient(object):
    """
    Redis数据库操作类。
    """

    def __init__(self, host=HOST, port=PORT):
        self._db = redis.Redis(host, port)

    def get(self, count=1):
        """从Pool中获取一定量数据。"""
        proxies = self._db.lrange("proxies", 0, count - 1)
        self._db.ltrim("proxies", count, -1)
        return proxies

    def put(self, proxy):
        """将代理压入Pool中。
        用Redis的set容器来负责去重，如果proxy能被压入proxy_set，
        就将其放入proxy pool中，否则不压入。
        """
        if self._db.sadd("set", proxy):
            self._db.rpush("proxies", proxy)
        else:
            pass

    def put_many(self, proxies):
        """将一定量的代理压入Pool。
        """
        for proxy in proxies:
            self.put(proxy)

    def pop(self):
        """弹出一个可用代理。
        """
        try:
            return self._db.blpop("proxies", 30)[1].decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        """获取proxy pool的大小。
        """
        return self._db.llen("proxies")

    def flush(self):
        """刷新Redis中的全部内容，测试用。
        """
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.get(20))
