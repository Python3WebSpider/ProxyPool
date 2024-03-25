from loguru import logger
from proxypool.storages.redis import RedisClient
from proxypool.setting import PROXY_NUMBER_MAX
from proxypool.crawlers import __all__ as crawlers_cls
from proxypool.testers import __all__ as testers_cls

class Getter(object):
    """
    getter of proxypool
    """

    def __init__(self):
        """
        init db and crawlers
        """
        self.redis = RedisClient()
        self.crawlers_cls = crawlers_cls
        self.crawlers = [crawler_cls() for crawler_cls in self.crawlers_cls]
        self.testers_cls = testers_cls
        self.testers = [tester_cls() for tester_cls in self.testers_cls]

    def is_full(self):
        """
        if proxypool if full
        return: bool
        """
        return self.redis.count() >= PROXY_NUMBER_MAX

    @logger.catch
    def run(self):
        """
        run crawlers to get proxy
        :return:
        """
        if self.is_full():
            return
        for crawler in self.crawlers:
            logger.info(f'crawler {crawler} to get proxy')
            for proxy in crawler.crawl():
                self.redis.add(proxy)
                [self.redis.add(proxy, redis_key=tester.key) for tester in self.testers]


if __name__ == '__main__':
    getter = Getter()
    getter.run()
