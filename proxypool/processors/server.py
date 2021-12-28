from flask import Flask, g , request , jsonify
from proxypool.storages.redis import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED,PROXY_SCORE_MIN, PROXY_SCORE_MAX


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
    """
    get home page, you can define your own templates
    :return:
    """
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    return conn.random().string()


@app.route('/all')
def get_proxy_all():
    """
    get proxy by min_score to max_score
    :return: proxies list
    """
    args = request.args
    conn = get_conn()
    proxies = conn.all(args.get('min_score',PROXY_SCORE_MIN),args.get('max_score',PROXY_SCORE_MAX))
    proxies_string = ''
    for proxy in proxies:
        proxies_string += str(proxy) + '\n'

    return proxies_string


@app.route('/count')
def get_count():
    """
    get the count of proxies
    :return: count, int
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
