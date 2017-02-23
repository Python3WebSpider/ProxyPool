from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    """
    爬虫的元类，在FreeProxyGetter类中加入
    __CrawlFunc__和__CrawlFuncCount__
    两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    """
    代理爬虫，负责扫描各大代理网站，抓取代理。
    该类有可扩展性，可根据需要自己添加新站点的代理抓取函数，
    但是函数名必须以crawl_开头，返回值必须以"host:port"的形式返回，
    添加器会自动识别并调用此类函数。
    """
    
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        抓取代理66网的数据。
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
        抓取proxy360网的数据。
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
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ', '')

    def crawl_haoip(self):
        start_url = 'http://haoip.cc/tiqu.htm'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            results = doc('.row .col-xs-12').html().split('<br/>')
            for result in results:
                if result: yield result.strip()
