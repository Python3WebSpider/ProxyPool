from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
import json


BASE_URL = 'https://ip.jiangxianli.com/api/proxy_ips?page={page}'

MAX_PAGE = 3


class JiangxianliCrawler(BaseCrawler):
    """
    jiangxianli crawler,https://ip.jiangxianli.com/
    """

    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """

        result = json.loads(html)
        if result['code'] != 0:
            return
        MAX_PAGE = int(result['data']['last_page'])
        hosts_ports = result['data']['data']
        for ip_address in hosts_ports:
            if(ip_address):
                host = ip_address['ip']
                port = ip_address['port']
                yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = JiangxianliCrawler()
    for proxy in crawler.crawl():
        print(proxy)
