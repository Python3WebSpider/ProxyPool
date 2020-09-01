import asyncio
import aiohttp
from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from loguru import logger

BASE_URL = 'http://www.data5u.com'


class Data5UCrawler(BaseCrawler):
    """
    data5u crawler, http://www.data5u.com
    """
    urls = [BASE_URL]

    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

    @logger.catch
    async def crawl(self):
        proxies = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            tasks = [self.fetch(session, url, headers=self.headers) for url in self.urls]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    for proxy in self.parse(result):
                        proxies.append(proxy)
            return proxies

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        items = doc('.wlist ul.l2').items()
        for item in items:
            host = item.find('span:first-child').text()
            port = int(item.find('span:nth-child(2)').text())
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = Data5UCrawler()
    for proxy in crawler.crawl():
        print(proxy)
