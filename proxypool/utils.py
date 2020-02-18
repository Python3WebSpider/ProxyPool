import requests
from requests.exceptions import ConnectionError
import re

from proxypool.proxy import Proxy


def parse_redis_connection_string(connection_string):
    """
    parse a redis connection string, for example:
    redis://[password]@host:port
    rediss://[password]@host:port
    :param connection_string:
    :return:
    """
    result = re.match('rediss?:\/\/(.*?)@(.*?):(\d+)', connection_string)
    return result.group(2), int(result.group(3)), (result.group(1) or None) if result \
        else ('localhost', 6379, None)


def is_valid_proxy(data):
    """
    is data is valid proxy format
    :param data:
    :return:
    """
    return re.match('\d+\.\d+\.\d+\.\d+\:\d+', data)


def convert_proxy_or_proxies(data):
    """
    convert list of str to valid proxies or proxy
    :param data:
    :return:
    """
    print(data)
    if not data:
        return None
    if isinstance(data, list):
        result = []
        for item in data:
            # skip invalid item
            item = item.strip()
            if not is_valid_proxy(item): continue
            host, port = item.split(':')
            result.append(Proxy(host=host, port=int(port)))
        return result
    if isinstance(data, str) and is_valid_proxy(data):
        host, port = data.split(':')
        return Proxy(host=host, port=int(port))
