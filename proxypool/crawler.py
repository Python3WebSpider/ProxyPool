import json

from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_xdaili(self):
        """
        获取讯代理
        :return: 代理
        """
        url = 'http://www.xdaili.cn/ipagent/greatRecharge/getGreatIp?spiderId=da289b78fec24f19b392e04106253f2a&orderno=YZ20177140586mTTnd7&returnType=2&count=20'
        html = get_page(url)
        if html:
            result = json.loads(html)
            proxies = result.get('RESULT')
            for proxy in proxies:
                yield proxy.get('ip') + ':' + proxy.get('port')

    def crawl_kuaidaili(self):
        """
        获取快代理
        :return: 代理
        """
        url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=959961765125099&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&quality=1&format=json&sep=2'
        html = get_page(url)
        if html:
            result = json.loads(html)
            proxies = result.get('data').get('proxy_list')
            for proxy in proxies:
                yield proxy

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_proxy360(self):
        """
        获取Proxy360
        :return: 代理
        """
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBottomLine:nth-child(2)').text()
                yield ':'.join([ip, port])

    def crawl_goubanjia(self):
        """
        获取Goubanjia
        :return: 代理
        """
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ', '')
