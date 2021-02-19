import asyncio
import aiohttp
from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
import re


BASE_URL = 'https://www.zdaye.com/dayProxy/{page}.html'
MAX_PAGE = 5


class ZhandayeCrawler(BaseCrawler):
    """
    zhandaye crawler, https://www.zdaye.com/dayProxy/
    """
    urls_catalog = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE)]
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }
    urls = []
    ignore = True

    async def crawl(self):
        await self.crawl_catalog()
        await super().crawl()

    async def crawl_catalog(self):
        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False)) as session:
            tasks = [self.fetch(session, url, headers=self.headers) for url in self.urls_catalog]
            results = await asyncio.gather(*tasks)
            for result in results:
                if result:
                    self.parse_catalog(result)

    def parse_catalog(self, html):
        """
        parse catalog_html file to get urls
        :return:
        """
        doc = pq(html)
        for item in doc('#J_posts_list .thread_item div div p a').items():
            url = 'https://www.zdaye.com' + item.attr('href')
            self.urls.append(url)

    def parse(self, html):
        doc = pq(html)
        trs = doc('.cont br').items()
        for tr in trs:
            line = tr[0].tail
            match = re.search(r'(\d+\.\d+\.\d+\.\d+):(\d+)', line)
            if match:
                host = match.group(1)
                port = match.group(2)
                yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = ZhandayeCrawler()
    for proxy in crawler.run():
        print(proxy)
