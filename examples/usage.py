import requests
import json
import random
from concurrent.futures import ThreadPoolExecutor
proxypool_url = 'http://127.0.0.1:5000/random'
target_url = 'http://httpbin.org/get'
with open("proxy.txt") as f:
    proxy_list = []
    for proxy in f:
        json_proxy = json.loads(proxy.strip())
        proxy_list.append(json_proxy["host"] + ":" + str(json_proxy["port"]))

print(proxy_list)


def get_random_proxy(source="url"):
    """
    get random proxy from proxypool
    :return: proxy
    """
    if source == "url":
        return requests.get(proxypool_url).text.strip()
    else:
        return random.choice(proxy_list)



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

def test_proxy():
    proxy = get_random_proxy("url")
    #print('get random proxy', proxy)
    resp = crawl(target_url, proxy)
    try:
        if resp:
            print(proxy, "origin:", resp.json().get("origin", ""), resp.headers.get("Via", ""))
            return True
        else:
            return False
    except Exception as e:
        print(e)
    return False


def main():
    """
    main method, entry point
    :return: none
    """
    threads = 100
    alive_count = 0
    pool = ThreadPoolExecutor(64)
    futures = [pool.submit(test_proxy) for i in range(threads)]
    for future in futures:
        res = future.result()
        if res:
            alive_count += 1
    print(alive_count)



if __name__ == '__main__':
    main()
