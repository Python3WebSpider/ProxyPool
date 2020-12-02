import cchardet
from loguru import logger
from retrying import retry
from requests import request, ConnectionError
from proxypool.setting import GET_TIMEOUT
from proxypool.crawlerTools.Ua import ua


class BaseCrawler(object):
    urls = []

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    def fetch(self, url, method=None, header=None, **kwargs):
        _method = "GET" if not method else method
        _header = {'User-Agent': ua()} if not header else header
        try:
            kwargs.setdefault('timeout', GET_TIMEOUT)
            kwargs.setdefault('verify', False)
            response = request(method=_method, url=url, headers=_header, **kwargs)
            print(_header)
            encoding = cchardet.detect(response.content)['encoding']
            if response.status_code == 200:
                return response.content.decode(encoding)
        except ConnectionError:
            return

    @logger.catch
    def crawl(self):
        """
        crawl main method
        """
        for url in self.urls:
            logger.info(f'fetching {url}')
            html = self.fetch(url)
            for proxy in self.parse(html):
                logger.info(f'fetched proxy {proxy.string()} from {url}')
                yield proxy
