import re
from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler

BASE_URL = "http://www.xsdaili.cn/"
PAGE_BASE_URL = "http://www.xsdaili.cn/dayProxy/ip/{page}.html"
MAX_PAGE = 3


class XiaoShuCrawler(BaseCrawler):
    """
    小舒代理 crawler, http://www.xsdaili.cn/
    """

    def __init__(self):
        """
        init urls
        """
        try:
            html = self.fetch(url=BASE_URL)
        except:
            self.urls = []
            return
        doc = pq(html)
        title = doc(".title:eq(0) a").items()
        latest_page = 0
        for t in title:
            res = re.search(r"/(\d+)\.html", t.attr("href"))
            latest_page = int(res.group(1)) if res else 0
        if latest_page:
            self.urls = [PAGE_BASE_URL.format(page=page) for page in range(
                latest_page - MAX_PAGE, latest_page)]
        else:
            self.urls = []

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        contents = doc('.cont').text()
        contents = contents.split("\n")
        for content in contents:
            c = content[:content.find("@")]
            host, port = c.split(":")
            yield Proxy(host=host, port=int(port))


if __name__ == '__main__':
    crawler = XiaoShuCrawler()
    for proxy in crawler.crawl():
        print(proxy)
