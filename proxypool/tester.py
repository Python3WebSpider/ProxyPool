import asyncio
import aiohttp

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db import RedisClient
from proxypool.setting import *


class Tester(object):
    def __init__(self):
        self.proxies = None
        self.redis = RedisClient()
    
    def set_proxies(self, proxies):
        """
        设置代理
        :param proxies:
        :return:
        """
        self.proxies = proxies
    
    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 
        :return: 
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.add(proxy)
                        print('代理可用', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('请求响应码不合法，IP', proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                if self.redis.exists(proxy):
                    self.redis.decrease(proxy)
                print('代理请求失败', proxy)
    
    def run(self):
        """
        测试主函数
        :return:
        """
        print('测试器开始运行')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in self.proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception as e:
            print('测试器发生错误', e.args)
