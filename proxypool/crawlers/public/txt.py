#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
from proxypool.crawlers.base import BaseCrawler
from proxypool.schemas.proxy import Proxy
import re
import retrying
import requests
from loguru import logger


class TxtProxy(BaseCrawler):
    def __init__(self):
        self.re_ip_port_pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):([\d]{1,5})")

        self.cur_proxy = None
        self.proxies = []
        self.result = []

        self.txt_list = [
            'http://static.fatezero.org/tmp/proxy.txt',
            'http://www.proxylists.net/http_highanon.txt',
            'http://www.proxylists.net/http.txt',
            'http://ab57.ru/downloads/proxylist.txt',
        ]

    @retrying.retry(stop_max_attempt_number=3)
    def extract_proxy(self, url):
        try:
            headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) "
                              "Chrome/21.0.1180.89 Safari/537.1'"
            }
            rp = requests.get(url, proxies=self.cur_proxy, headers=headers, timeout=10)

            re_ip_port_result = self.re_ip_port_pattern.findall(rp.text)

            if not re_ip_port_result:
                raise Exception("empty")

        except Exception as e:
            logger.error("[-] Request url {url} error: {error}".format(url=url, error=str(e)))
            while self.proxies:
                new_proxy = self.proxies.pop(0)
                self.cur_proxy = {new_proxy['type']: "%s:%s" % (new_proxy['host'], new_proxy['port'])}
                raise e
            else:
                return []

        return [{'host': host, 'port': int(port), 'from': 'txt'} for host, port in re_ip_port_result]

    def crawl(self):
        for url in self.txt_list:
            try:
                page_result = self.extract_proxy(url)
                self.result.extend(page_result)
                for item in page_result:
                    logger.info(f'{item["host"]}:{item["port"]}')
                    yield Proxy(host=item["host"], port=item["port"])
            except:
                continue

            if not page_result:
                continue

if __name__ == '__main__':
    p = TxtProxy()

    for i in p.crawl():
        print(i)

