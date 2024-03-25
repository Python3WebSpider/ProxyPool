from flask import Flask, g, request
from proxypool.exceptions import PoolEmptyException
from proxypool.storages.redis import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED, API_KEY, IS_DEV, PROXY_RAND_KEY_DEGRADED
import functools

__all__ = ['app']

app = Flask(__name__)
if IS_DEV:
    app.debug = True


def auth_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # conditional decorator, when setting API_KEY is set, otherwise just ignore this decorator
        if API_KEY == "":
            return func(*args, **kwargs)
        if request.headers.get('API-KEY', None) is not None:
            api_key = request.headers.get('API-KEY')
        else:
            return {"message": "Please provide an API key in header"}, 400
        # Check if API key is correct and valid
        if request.method == "GET" and api_key == API_KEY:
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403

    return decorator


def get_conn():
    """
    get redis client object
    :return:
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
@auth_required
def index():
    """
    get home page, you can define your own templates
    :return:
    """
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
@auth_required
def get_proxy():
    """
    get a random proxy, can query the specific sub-pool according the (redis) key
    if PROXY_RAND_KEY_DEGRADED is set to True, will get a universal random proxy if no proxy found in the sub-pool
    :return: get a random proxy
    """
    key = request.args.get('key')
    conn = get_conn()
    # return conn.random(key).string() if key else conn.random().string()
    if key:
        try:
            return conn.random(key).string()
        except PoolEmptyException:
            if not PROXY_RAND_KEY_DEGRADED:
                raise
    return conn.random().string()


@app.route('/all')
@auth_required
def get_proxy_all():
    """
    get a random proxy
    :return: get a random proxy
    """
    key = request.args.get('key')

    conn = get_conn()
    proxies = conn.all(key) if key else conn.all()
    proxies_string = ''
    if proxies:
        for proxy in proxies:
            proxies_string += str(proxy) + '\n'

    return proxies_string


@app.route('/count')
@auth_required
def get_count():
    """
    get the count of proxies
    :return: count, int
    """
    conn = get_conn()
    key = request.args.get('key')
    return str(conn.count(key)) if key else conn.count()


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
