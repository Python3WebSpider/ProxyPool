from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
import re

MAX_NUM = 9999
BASE_URL = 'http://api.89ip.cn/tqdl.html?api=1&num={MAX_NUM}&port=&address=&isp='.format(MAX_NUM=MAX_NUM)


class Ip89Crawler(BaseCrawler):
    """
    89ip crawler, http://api.89ip.cn
    """
    urls = [BASE_URL]
    
    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        ip_address = re.compile('([\d:\.]*)<br>')
        hosts_ports = ip_address.findall(html)
        for addr in hosts_ports:
            addr_split = addr.split(':')
            if(len(addr_split) == 2):
                host = addr_split[0]
                port = addr_split[1]
                yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = Ip89Crawler()
    for proxy in crawler.crawl():
        print(proxy)
