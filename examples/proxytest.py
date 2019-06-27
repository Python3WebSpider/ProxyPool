import requests
from proxypool.setting import TEST_URL_LIST

proxy = '96.9.90.90:8080'

proxies = {
    'http': 'http://' + proxy,
    'https': 'https://' + proxy,
}


for test_url in TEST_URL_LIST:
    response = requests.get(test_url, proxies=proxies, verify=False)
    if response.status_code == 200:
        print('Successfully Tested Url: {}'.format(test_url))
        print(response.text)
