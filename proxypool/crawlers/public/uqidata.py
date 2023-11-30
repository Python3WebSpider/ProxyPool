from pyquery import PyQuery as pq
from proxypool.schemas.proxy import Proxy
from proxypool.crawlers.base import BaseCrawler
from loguru import logger

BASE_URL = 'https://ip.uqidata.com/free/index.html'


class UqidataCrawler(BaseCrawler):
    """
    Uqidata crawler, https://ip.uqidata.com/free/index.html
    """
    urls = [BASE_URL]
    ignore = True

    def encode(input_str):
        tmp = []
        for i in range(len(input_str)):
            tmp.append("ABCDEFGHIZ".find(input_str[i]))
        result = "".join(str(i) for i in tmp)
        result = int(result) >> 0x03
        return result

    def parse(self, html):
        """
        parse html file to get proxies
        :return:
        """
        doc = pq(html)
        trs = doc('#main_container .inner table tbody tr:nth-child(n+3)').items()
        for tr in trs:
            ip_html = tr('td.ip').find("*").items()
            host = ''
            for i in ip_html:
                if i.attr('style') is not None and 'none' in i.attr('style'):
                    continue
                if i.text() == '':
                    continue
                host += i.text()

            port_code = tr('td.port').attr('class').split(' ')[1]
            port = UqidataCrawler.encode(port_code)
            yield Proxy(host=host, port=port)


if __name__ == '__main__':
    crawler = UqidataCrawler()
    for proxy in crawler.crawl():
        print(proxy)
