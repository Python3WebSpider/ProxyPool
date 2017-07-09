import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.setting import MAX_SCORE, MIN_SCORE
from random import choice


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host:
        :param port:
        :param password:
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password)
    
    def top(self):
        """
        获取排名第一的代理
        :return:
        """
        proxies = self.db.zrevrange(REDIS_KEY, 0, 0)
        if proxies:
            return proxies[0].decode('utf-8')
        else:
            raise PoolEmptyError
    
    def add(self, proxy, score=MAX_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy:
        :param score:
        :return:
        """
        return self.db.zadd(REDIS_KEY, score, proxy)
    
    def random(self):
        """
        随机获取有效代理
        :return:
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result).decode('utf-8')
        else:
            raise PoolEmptyError
    
    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy:
        :return:
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            self.db.zincrby(REDIS_KEY, proxy, -1)
            print('代理', proxy, '当前分数', score, '减1')
        else:
            self.db.zrem(REDIS_KEY, proxy)
            print('代理', proxy, '当前分数', score, '移除')
    
    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 
        :return: 
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None
    
    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy:
        :return:
        """
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)
    
    def count(self):
        """
        获取数量
        :return:
        """
        return self.db.zcard(REDIS_KEY)
    
    def all(self):
        """
        获取全部代理
        :return:
        """
        all = self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
        return [item.decode('utf-8') for item in all]
    

if __name__ == '__main__':
    conn = RedisClient()
    result = conn.all()
    print(result)
    random = conn.random()
    print('Random', random)
    top = conn.top()
    print('Top', top)
    conn.decrease('a')
