from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from pyquery import PyQuery as pq

BaseUrl = 'https://www.fanqieip.com/free/{num}'
MAX_PAGE = 5 * 100


class FanqieIPCrawler(BaseCrawler):
    """
    FanqieIP crawler, https://www.fanqieip.com
    """
    urls = [BaseUrl.format(num=i) for i in range(1, MAX_PAGE)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('.layui-table tbody tr ').items()
        for tr in trs:
            host = tr.find('td div')[0].text
            port = tr.find('td div')[1].text
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = FanqieIPCrawler()
    for proxy in crawler.crawl():
        print(proxy)
