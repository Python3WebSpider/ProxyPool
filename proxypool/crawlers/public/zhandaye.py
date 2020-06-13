from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from loguru import logger


BASE_URL = 'https://www.zdaye.com/dayProxy/{page}.html'
MAX_PAGE = 5

class ZhandayeCrawler(BaseCrawler):
    """
    zhandaye crawler, https://www.zdaye.com/dayProxy/
    """
    urls = [BASE_URL.format(page=page) for page in range(1, MAX_PAGE)]

    def crawl(self):
        for url in self.urls:
            logger.info(f'fetching {url}')
            if not self.headers:
                html = self.fetch(url)
            else:
                html = self.fetch(url, headers=self.headers)
            self.parse(html)

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        for item in doc('#J_posts_list .thread_item div div p a').items():
            post = 'https://www.zdaye.com' + item.attr('href')
            logger.info(f'get detail url: {post}')
            ZhandayeDetailCrawler(post).crawl()


class ZhandayeDetailCrawler(BaseCrawler):
    urls = []
    ignore = True

    def __init__(self, url):
        self.urls.append(url)
        super().__init__()

    def parse(self, html):
        doc = pq(html)
        trs = doc('.cont br').items()
        for tr in trs:
            line = tr[0].tail
            host = line.split(':')[0]
            port = line.split(':')[1][:4]
            yield Proxy(host=host, port=port)



if __name__ == '__main__':
    crawler = ZhandayeCrawler()
    for proxy in crawler.crawl():
        print(proxy)