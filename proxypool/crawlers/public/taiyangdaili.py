from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from pyquery import PyQuery as pq

BaseUrl = 'http://www.taiyanghttp.com/free/page{num}'
MAX_PAGE = 3


class TaiyangdailiCrawler(BaseCrawler):
    """
    taiyangdaili crawler, http://www.taiyanghttp.com/free/
    """
    urls = [BaseUrl.format(num=i) for i in range(1, 6)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('#ip_list .tr.ip_tr').items()
        for tr in trs:
            host = tr.find('div:nth-child(1)').text()
            port = tr.find('div:nth-child(2)').text()
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = TaiyangdailiCrawler()
    for proxy in crawler.crawl():
        print(proxy)
