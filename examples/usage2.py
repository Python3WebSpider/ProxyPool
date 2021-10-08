# -*- coding: UTF-8 -*-

'''
'''
import requests
import time
import threading
import urllib3
from fake_headers import Headers
import uuid
from geolite2 import geolite2
ips = []

# 爬数据的线程类

def getChinaIP(ip='127.0.0.1'):
    reader = geolite2.reader()
    ip_info = reader.get(ip)
    geolite2.close()
    print(ip_info)
    return True if ip_info['country']['iso_code'] == 'CN' else False



class CrawlThread(threading.Thread):
    def __init__(self, proxyip):
        super(CrawlThread, self).__init__()
        self.proxyip = proxyip

    def run(self):
        # 开始计时
        pure_ip_address = self.proxyip.split(':')[0]
        # 验证IP归属
        if not getChinaIP(pure_ip_address):
            # pass
            raise ValueError('不是有效IP')
        # 
        start = time.time()
        # 消除关闭证书验证的警告
        urllib3.disable_warnings()
        headers = Headers(headers=True).generate()
        headers['Referer'] = 'http://bb.cf08tp.cn/Home/index.php?m=Index&a=index&id=2676'
        headers['Pragma'] = 'no-cache'
        headers['Host'] = 'bb.cf08tp.cn'
        headers['x-forward-for'] = pure_ip_address
        headers['Cookie'] = 'PHPSESSID={}'.format(
            ''.join(str(uuid.uuid1()).split('-')))
        print(headers)
        html = requests.get(headers=headers, url=targetUrl, proxies={
                            "http": 'http://' + self.proxyip, "https": 'https://' + self.proxyip}, verify=False, timeout=2).content.decode()
        # 结束计时
        end = time.time()
        # 输出内容
        print(threading.current_thread().getName() + "使用代理IP, 耗时 " + str(end - start) +
              "毫秒 " + self.proxyip + " 获取到如下HTML内容：\n" + html + "\n*************")

# 获取代理IP的线程类


class GetIpThread(threading.Thread):
    def __init__(self, fetchSecond):
        super(GetIpThread, self).__init__()
        self.fetchSecond = fetchSecond

    def run(self):
        global ips
        while True:
            # 获取IP列表
            res = requests.get(apiUrl).content.decode()
            # 按照\n分割获取到的IP
            ips = res.split('\n')
            # 利用每一个IP
            for proxyip in ips:
                if proxyip.strip():
                    # 开启一个线程
                    # CrawlThread(proxyip).start()
                    try:
                        CrawlThread(proxyip).run()
                        time.sleep(1.5)
                    except Exception as e:
                        print(e)
            # 休眠
            time.sleep(len(ips) /self.fetchSecond )


if __name__ == '__main__':
    # 获取IP的API接口
    # apiUrl = "http://127.0.0.1:5555/all"
    apiUrl = "http://127.0.0.1:5555/random"
    # 要抓取的目标网站地址
    targetUrl = "http://bb.cf08tp.cn/Home/index.php?m=Index&a=vote&vid=335688&id=2676&tp="
    # targetUrl = 'http://bb.cf08tp.cn/Home/index.php?m=Index&a=vote&vid=335608&id=2676&tp='
    fetchSecond = 5
    # 开始自动获取IP
    GetIpThread(fetchSecond).start()
