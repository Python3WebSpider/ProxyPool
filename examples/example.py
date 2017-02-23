import os
import sys
import requests
from bs4 import BeautifulSoup
import lxml
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Before run this example, Please run 'run.py'.!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def get_proxy():
    r = requests.get('http://127.0.0.1:5000/get')
    proxy = BeautifulSoup(r.text, "lxml").get_text()
    return proxy


def crawl(url, proxy):
    proxies = {'http': proxy}
    r = requests.get(url, proxies=proxies)
    return r.text


def main():
    proxy = get_proxy()
    html = crawl('http://docs.jinkan.org/docs/flask/', proxy)
    print(html)

if __name__ == '__main__':
    main()
