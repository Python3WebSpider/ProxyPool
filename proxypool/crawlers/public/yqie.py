from pyquery import PyQuery as pq

from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = "http://ip.yqie.com/ipproxy.htm"
MAX_PAGE = 1


class YqIeCrawler(BaseCrawler):
    """
    ip yqie crawler, http://ip.yqie.com/ipproxy.htm
    """
    urls = [BASE_URL]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('#GridViewOrder tr:gt(0)').items()
        for tr in trs:
            host = tr.find('td:nth-child(1)').text()
            port = int(tr.find('td:nth-child(2)').text())
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = YqIeCrawler()
    for proxy in crawler.crawl():
        print(proxy)
