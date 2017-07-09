import requests

from proxypool.db import RedisClient

conn = RedisClient()


def set(proxy):
    result = conn.add(proxy)
    print(proxy)
    print('录入成功' if result else '录入失败')


def scan():
    print('请输入代理, 输入exit退出读入')
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)


if __name__ == '__main__':
    scan()
