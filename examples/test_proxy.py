#!/usr/bin/env python
#coding:utf-8

import json
import requests

proxypool_url = 'http://127.0.0.1:5000/random'
target_url = 'http://httpbin.org/get'

def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()

def crawl(url, proxy):
    """
    use proxy to crawl page
    :param url: page url
    :param proxy: proxy, such as 8.8.8.8:8888
    :return: html
    """
    proxies = {'http': 'http://' + proxy}
    try:
        resp = requests.get(url, proxies=proxies, timeout=20)
        return resp
    except Exception as e:
        print(e)
    return False


if __name__ == '__main__':
    proxy_list = [
        #"36.248.129.176:9999",
        "171.35.223.122:9999"
    ]
    for proxy in proxy_list:
        # proxy = get_random_proxy()
        resp = crawl(target_url, proxy)
        print(resp.json())
        print(resp.headers)

# def _check_proxy_anonymity(self, response):
#     via = response.get('headers', {}).get('Via', '')
#
#     if self.origin_ip in json.dumps(response):
#         return 'transparent'
#     elif via and via != "1.1 vegur":
#         return 'anonymous'
#     else:
#         return 'high_anonymous'