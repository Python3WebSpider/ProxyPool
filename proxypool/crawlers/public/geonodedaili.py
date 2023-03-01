import time
from retrying import RetryError
from loguru import logger
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
import json

BASE_URL = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page={page}&sort_by=lastChecked&sort_type=desc'
MAX_PAGE = 18


class GeonodeCrawler(BaseCrawler):
    """
    Geonode crawler, https://proxylist.geonode.com/
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE + 1)]

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        try:
            result = json.loads(html)
            proxy_list = result['data']
            for proxy_item in proxy_list:
                host = proxy_item['ip']
                port = proxy_item['port']
                yield Proxy(host=host, port=port)
        except json.JSONDecodeError:
            print("json.JSONDecodeError")
            return

    def crawl(self):
        """
        override crawl main method
        add headers
        """
        headers = {
            'authority': 'proxylist.geonode.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            'accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
            'sec-ch-ua-platform': '"macOS"',
            'origin': 'https://geonode.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://geonode.com/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            'if-none-match': 'W/"c25d-BXjLTmP+/yYXtIz4OEcmdOWSv88"',
        }
        try:
            for url in self.urls:
                logger.info(f'fetching {url}')
                html = self.fetch(url, headers=headers)
                if not html:
                    continue
                time.sleep(.5)
                yield from self.process(html, url)
        except RetryError:
            logger.error(
                f'crawler {self} crawled proxy unsuccessfully, '
                'please check if target url is valid or network issue')


if __name__ == '__main__':
    crawler = GeonodeCrawler()
    for proxy in crawler.crawl():
        print(proxy)
