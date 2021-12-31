from proxypool.crawlers.base import BaseCrawler
from proxypool.schemas.proxy import Proxy
import re


MAX_PAGE = 3
BASE_URL = 'http://www.ip3366.net/free/?stype={stype}&page={page}'


class IP3366Crawler(BaseCrawler):
    """
    ip3366 crawler, http://www.ip3366.net/
    """
    urls = [BASE_URL.format(stype=stype,page=i) for stype in range(1,3) for i in range(1, 8)]
    
    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        # \s * 匹配空格，起到换行作用
        re_ip_address = ip_address.findall(html)
        for address, port in re_ip_address:
            proxy = Proxy(host=address.strip(), port=int(port.strip()))
            yield proxy


if __name__ == '__main__':
    crawler = IP3366Crawler()
    for proxy in crawler.crawl():
        print(proxy)
