import requests
import re
import execjs
from requests.exceptions import RequestException


class Crawl_66ip:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/63.0.3239.132 Safari/537.36'
        }

    # 获取目标页面
    def get_url(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.text
            elif resp.status_code == 521:
                cookie_part = self.get_521_content(resp)
                cookie_id = cookie_part[0]
                cookie_js = self.parse_js(cookie_part[1])
                self.headers['Cookie'] = cookie_id+';'+cookie_js
                return self.get_url(url)
            else:
                return None
        except RequestException:
            print('请求页面失败！')

    # 获取js代码、和cookie_id部分
    def get_521_content(self, response):
        cookies = response.cookies
        cookies = '; '.join(['='.join(item) for item in cookies.items()])
        js_content = response.text
        js_content = ''.join(re.findall('<script>(.*?)</script>', js_content))
        return cookies, js_content

    # 解析js代码，提取cookie_js部分
    def parse_js(self, content):
        # 把js代码中所有的关键字‘eval’替换成‘return’
        # 执行一次替换后的js代码
        # 调用call方法执行里面定义了的一个名为‘f’的函数，返回一段新的js代码
        content = content.replace('eval', 'return')
        once_content = execjs.compile(content)
        twice_content = once_content.call('f')
        # （新的js代码中定义的函数的名字不是每次都一样），通过正则表达式匹配出来
        func_name = re.search(r'(_.*?)=function()', twice_content).group(1)
        # 补充定义js代码中缺少的‘window’对象
        # 去除语法错误（代码中有两个‘return’）
        # 替换掉关于‘document’对象的内容
        twice_content = re.sub("=function.*?__jsl_clearance=", "=function(){var window={};return '__jsl_clearance=", twice_content)
        twice_content = re.sub(r"{return return\('String.fromCharCode\(", "{return ('String.fromCharCode(", twice_content)
        twice_content = re.sub('document\.createElement.*?toLowerCase\(\)', '"www.66ip.cn/"', twice_content)
        # 过滤掉js代码中的无关信息
        thrice_content = twice_content.replace(r"setTimeout('location.href=location.pathname+\
        location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);",'').\
            replace('document.cookie=','return ').replace(';if((function(){try{return !!window.addEventListener;}','').\
            replace("catch(e){return false;}})()){document.addEventListener('DOMContentLoaded',"+func_name+",false)}",'').\
            replace("else{document.attachEvent('onreadystatechange',"+func_name+")}",'')
        result = execjs.compile(thrice_content)
        # 执行js里的函数，返回cookie_js的值
        cookies = result.call(func_name)
        __jsl_clearance = cookies.split(';')[0]
        return __jsl_clearance
