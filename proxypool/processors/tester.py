import asyncio
import aiohttp
from loguru import logger
from proxypool.schemas import Proxy
from proxypool.storages.redis import RedisClient
from proxypool.setting import TEST_TIMEOUT, TEST_BATCH, TEST_URL, TEST_VALID_STATUS, TEST_ANONYMOUS, \
    TEST_DONT_SET_MAX_SCORE
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from asyncio import TimeoutError
from proxypool.testers import __all__ as testers_cls

EXCEPTIONS = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError,
    AssertionError
)


class Tester(object):
    """
    tester for testing proxies in queue
    """

    def __init__(self):
        """
        init redis
        """
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()
        self.testers_cls = testers_cls
        self.testers = [tester_cls() for tester_cls in self.testers_cls]

    async def test(self, proxy: Proxy):
        """
        test single proxy
        :param proxy: Proxy object
        :return:
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                logger.debug(f'testing {proxy.string()}')
                # if TEST_ANONYMOUS is True, make sure that
                # the proxy has the effect of hiding the real IP
                # logger.debug(f'TEST_ANONYMOUS {TEST_ANONYMOUS}')
                if TEST_ANONYMOUS:
                    url = 'https://httpbin.org/ip'
                    async with session.get(url, timeout=TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        origin_ip = resp_json['origin']
                        # logger.debug(f'origin ip is {origin_ip}')
                    async with session.get(url, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        anonymous_ip = resp_json['origin']
                        logger.debug(f'anonymous ip is {anonymous_ip}')
                    assert origin_ip != anonymous_ip
                    assert proxy.host == anonymous_ip
                async with session.get(TEST_URL, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT,
                                       allow_redirects=False) as response:
                    if response.status in TEST_VALID_STATUS:
                        if TEST_DONT_SET_MAX_SCORE:
                            logger.debug(
                                f'proxy {proxy.string()} is valid, remain current score')
                        else:
                            self.redis.max(proxy)
                            logger.debug(
                                f'proxy {proxy.string()} is valid, set max score')
                    else:
                        self.redis.decrease(proxy)
                        logger.debug(
                            f'proxy {proxy.string()} is invalid, decrease score')
                # if independent tester class found, create new set of storage and do the extra test
                for tester in self.testers:
                    key = tester.key
                    if self.redis.exists(proxy, key):
                        test_url = tester.test_url
                        headers = tester.headers()
                        cookies = tester.cookies()
                        async with session.get(test_url, proxy=f'http://{proxy.string()}',
                                               timeout=TEST_TIMEOUT,
                                               headers=headers,
                                               cookies=cookies,
                                               allow_redirects=False) as response:
                            resp_text = await response.text()
                            is_valid = await tester.parse(resp_text, test_url, proxy.string())
                            if is_valid:
                                if tester.test_dont_set_max_score:
                                    logger.info(
                                        f'key[{key}] proxy {proxy.string()} is valid, remain current score')
                                else:
                                    self.redis.max(
                                        proxy, key, tester.proxy_score_max)
                                    logger.info(
                                        f'key[{key}] proxy {proxy.string()} is valid, set max score')
                            else:
                                self.redis.decrease(
                                    proxy, tester.key, tester.proxy_score_min)
                                logger.info(
                                    f'key[{key}] proxy {proxy.string()} is invalid, decrease score')

            except EXCEPTIONS:
                self.redis.decrease(proxy)
                [self.redis.decrease(proxy, tester.key, tester.proxy_score_min)
                 for tester in self.testers]
                logger.debug(
                    f'proxy {proxy.string()} is invalid, decrease score')

    @logger.catch
    def run(self):
        """
        test main method
        :return:
        """
        # event loop of aiohttp
        logger.info('stating tester...')
        count = self.redis.count()
        logger.debug(f'{count} proxies to test')
        cursor = 0
        while True:
            logger.debug(
                f'testing proxies use cursor {cursor}, count {TEST_BATCH}')
            cursor, proxies = self.redis.batch(cursor, count=TEST_BATCH)
            if proxies:
                tasks = [self.loop.create_task(
                    self.test(proxy)) for proxy in proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
            if not cursor:
                break


def run_tester():
    host = '96.113.165.182'
    port = '3128'
    tasks = [tester.test(Proxy(host=host, port=port))]
    tester.loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    tester = Tester()
    tester.run()
    # run_tester()
