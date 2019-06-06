# ProxyPool

## 安装

### 安装Python

至少Python3.5以上

### 安装Redis

安装好之后将Redis服务开启

### 配置代理池

```
cd proxypool
```

进入proxypool目录，修改settings.py文件

PASSWORD为Redis密码，如果为空，则设置为None

#### 安装依赖

```
pip3 install -r requirements.txt
```

##### 使用`pipenv`安装依赖

```
pipenv install
# 关于依赖
#     * 由于`falsk`1.0以上版本的启动方式发生改变, 如果你不存在特殊需求, 推荐你使用`0.11.1`版本.
#     * 其他依赖可以按需升级的最新版本
```

#### 打开代理池和API

```
python3 run.py
```

## 获取代理


利用requests获取方法如下

```python
import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
```
