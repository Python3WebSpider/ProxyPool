import asyncio
import aiohttp
from loguru import logger
from proxypool.schemas import Proxy
from proxypool.storages.redis import RedisClient
from proxypool.setting import TEST_TIMEOUT, TEST_BATCH, TEST_URL, TEST_VALID_STATUS, TEST_ANONYMOUS
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from asyncio import TimeoutError


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

    async def test(self, session, proxy: Proxy):
        """
        test single proxy
        :param proxy: Proxy object
        :return:
        """
        try:
            logger.debug(f'testing {proxy.string()}')
            # if TEST_ANONYMOUS is True, make sure that
            # the proxy has the effect of hiding the real IP
            if TEST_ANONYMOUS:
                url = 'https://httpbin.org/ip'
                async with session.get(url, timeout=TEST_TIMEOUT) as response:
                    resp_json = await response.json()
                    origin_ip = resp_json['origin']
                async with session.get(url, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT) as response:
                    resp_json = await response.json()
                    anonymous_ip = resp_json['origin']
                assert origin_ip != anonymous_ip
                assert proxy.host == anonymous_ip
            async with session.get(TEST_URL, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT,
                                    allow_redirects=False) as response:
                if response.status in TEST_VALID_STATUS:
                    self.redis.max(proxy)
                    logger.debug(f'proxy {proxy.string()} is valid, set max score')
                else:
                    self.redis.decrease(proxy)
                    logger.debug(f'proxy {proxy.string()} is invalid, decrease score')
        except EXCEPTIONS:
            self.redis.decrease(proxy)
            logger.debug(f'proxy {proxy.string()} is invalid, decrease score')

    @logger.catch
    async def main(self):
        """
        test main method
        :return:
        """
        # event loop of aiohttp
        logger.info('stating tester...')
        count = self.redis.count()
        logger.debug(f'{count} proxies to test')
        cursor = 0
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            while True:
                logger.debug(f'testing proxies use cursor {cursor}, count {TEST_BATCH}')
                cursor, proxies = self.redis.batch(cursor, count=TEST_BATCH)
                if proxies:
                    tasks = [self.test(session, proxy) for proxy in proxies]
                    await asyncio.gather(*tasks)
                if not cursor:
                    break

    def run(self):
        self.loop.run_until_complete(self.main())


if __name__ == '__main__':
    tester = Tester()
    tester.run()
