import asyncio
import aiohttp
import time
import sys
import ssl

from aiohttp import ClientError
from aiohttp.client_exceptions import ClientProxyConnectionError, ClientConnectionError, ClientConnectorSSLError, ClientSSLError

from proxypool.db import RedisClient
from proxypool.setting import *

import logging
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(message)s"
logging.basicConfig(format=fmt, level=logging.INFO)


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()
    
    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy:
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        try:
            async with aiohttp.ClientSession(connector=conn) as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    # print('正在测试', proxy)
                    logging.debug({'Testing': proxy})
                    for test_url in TEST_URL_LIST:
                        async with session.get(test_url, proxy=real_proxy, timeout=TEST_TIMEOUT, allow_redirects=False,
                                               headers={'User-Agent': USER_AGENT}) as response:
                            if response.status in VALID_STATUS_CODES:
                                self.redis.max(proxy)
                                # print('代理可用', proxy)
                            else:
                                self.redis.decrease(proxy)
                                logging.info({'Status Invalid': response.status, 'IP': proxy})
                                # print('请求响应码不合法 ', response.status, 'IP', proxy)
                except (ClientError, ClientConnectionError, ClientProxyConnectionError, ClientSSLError, ClientConnectorSSLError,
                        asyncio.TimeoutError, ssl.SSLError,) as e:
                    self.redis.decrease(proxy)
                    logging.info({'Failed': proxy, 'Reason': e})
                    # print('代理请求失败', proxy)
        except Exception as e:
            logging.warning(e)
    
    def run(self):
        """
        测试主函数
        :return:
        """
        logging.info('测试器开始运行')
        try:
            count = self.redis.count()
            logging.info({'Surplus': count})
            # print('当前剩余', count, '个代理')
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                logging.debug({'Testing {} - {}'.format(start, stop)})
                # print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = self.redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            logging.error({'测试器发生错误': str(e.args)})
