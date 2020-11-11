from loguru import logger
from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'http://www.data5u.com'


class Data5UCrawler(BaseCrawler):
    """
    data5u crawler, http://www.data5u.com
    """
    urls = [BASE_URL]

    @logger.catch
    def crawl(self):
        """
        crawl main method
        """
        for url in self.urls:
            logger.info(f'fetching {url}')
            html = self.fetch(url)
            for proxy in self.parse(html):
                logger.info(f'fetched proxy {proxy.string()} from {url}')
                yield proxy

    @staticmethod
    def parse(html):
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
