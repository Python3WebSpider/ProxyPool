import re
from loguru import logger
from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'https://www.zdaye.com/dayProxy/{page}.html'
MAX_PAGE = 5


class ZhandayeCrawler(BaseCrawler):
    """
    zhandaye crawler, https://www.zdaye.com/dayProxy/
    """
    urls_catalog = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE)]
    urls = []
    ignore = True

    def crawl(self):
        self.crawl_catalog()
        yield from super().crawl()

    def crawl_catalog(self):
        for url in self.urls_catalog:
            logger.info(f'fetching {url}')
            html = self.fetch(url)
            self.parse_catalog(html)

    def parse_catalog(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        for item in doc('#J_posts_list .thread_item div div p a').items():
            url = 'https://www.zdaye.com' + item.attr('href')
            logger.info(f'get detail url: {url}')
            self.urls.append(url)

    @staticmethod
    def parse(html):
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
    for proxy in crawler.crawl():
        print(proxy)
