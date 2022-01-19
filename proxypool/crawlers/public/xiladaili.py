from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from lxml import etree

BASE_URL = "http://www.xiladaili.com/"
MAX_PAGE = 5


class XiladailiCrawler(BaseCrawler):
    """
    xiladaili crawler, http://www.xiladaili.com/
    """
    urls = ["http://www.xiladaili.com/"]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        etree_html = etree.HTML(html)
        ip_ports = etree_html.xpath("//tbody/tr/td[1]/text()")

        for ip_port in ip_ports:
            host = ip_port.partition(":")[0]
            port = ip_port.partition(":")[2]
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = XiladailiCrawler()
    for proxy in crawler.crawl():
        print(proxy)
