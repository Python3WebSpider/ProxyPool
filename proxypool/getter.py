from proxypool.tester import Tester
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
from proxypool.setting import *


class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.tester = Tester()
        self.crawler = Crawler()
    
    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False
    
    def run(self):
        print('获取器开始执行')
        proxy_count = 0
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                # 设置代理并测试
                self.tester.set_proxies(proxies)
                self.tester.run()
                proxy_count += len(proxies)
                if self.is_over_threshold():
                    print('代理池已满，暂停抓取')
                    break
            if proxy_count == 0:
                # 代理池枯竭
                print('代理池已枯竭')