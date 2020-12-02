from parsel import Selector
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = 'https://ip.jiangxianli.com/?page={page}&country=%E4%B8%AD%E5%9B%BD'
MAX_PAGE = 3


class Jiangxianli(BaseCrawler):
    """
    Jiangxianli Crawler:https://ip.jiangxianli.com
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]

    @staticmethod
    def parse(html):
        """
        parse html file to get proxies
        :return:
        """
        selector = Selector(html)
        trs = selector.css("table.layui-table > tbody > tr")
        for tr in trs:
            host = tr.css("td:nth-child(1)::text").extract_first()
            port = tr.css("td:nth-child(2)::text").extract_first()
            yield Proxy(host, port)


if __name__ == '__main__':
    crawler = Jiangxianli()
    for proxy in crawler.crawl():
        print(proxy)
