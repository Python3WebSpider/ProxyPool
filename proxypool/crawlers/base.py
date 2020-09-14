import asyncio
import aiohttp
from retrying import retry
from loguru import logger
from proxypool.setting import GET_TIMEOUT


class BaseCrawler(object):
    urls = []

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    async def fetch(self, session, url, **kwargs):
        try:
            kwargs.setdefault('timeout', GET_TIMEOUT)
            async with session.get(url, **kwargs) as response:
                if response.status == 200:
                    response.encoding = 'utf-8'
                    return await response.text()
        except aiohttp.ClientConnectionError:
            return

    @logger.catch
    async def crawl(self):
        """
        crawl main method
        """
        proxies = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            tasks = [self.fetch(session, url) for url in self.urls]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    for proxy in self.parse(result):
                        proxies.append(proxy)
            return proxies

    def run(self):
        return self.loop.run_until_complete(self.crawl())
