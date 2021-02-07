from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
import re
from pyquery import PyQuery as pq
import time
BASE_URL = 'https://ip.ihuan.me/today/{path}.html'


class IhuanCrawler(BaseCrawler):
    """
    ip  ihuan crawler, https://ip.ihuan.me
    """
    path = time.strftime("%Y/%m/%d/%H", time.localtime())
    urls = [BASE_URL.format(path=path)]
    ignore = False
    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        # doc = pq(html)('.text-left')
        ip_address = re.compile('([\d:\.]*).*?<br>')
        hosts_ports = ip_address.findall(html)
        for addr in hosts_ports:
            addr_split = addr.split(':')
            if(len(addr_split) == 2):
                host = addr_split[0]
                port = addr_split[1]
                yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = IhuanCrawler()
    for proxy in crawler.crawl():
        print(proxy)
