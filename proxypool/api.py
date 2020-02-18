from flask import Flask, g
from .db import RedisClient
from .setting import API_HOST, API_PORT

__all__ = ['app']

app = Flask(__name__)

def get_conn():
    """
    get redis client object
    :return:
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'

@app.route('/random')
def get_proxy():
    """
    get a random proxy
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_counts():
    """
    get the count of proxies
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=True)
