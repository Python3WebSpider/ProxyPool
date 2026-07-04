import hmac
import re
from flask import Flask, g, request, abort
from proxypool.exceptions import PoolEmptyException
from proxypool.storages.redis import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED, API_KEY, IS_DEV, PROXY_RAND_KEY_DEGRADED
import functools

__all__ = ['app']

app = Flask(__name__)
if IS_DEV:
    app.debug = True

# allowed characters for the `key` query parameter that selects a redis sub-pool;
# restricts to a safe charset to avoid probing arbitrary redis keys via the API
VALID_KEY_PATTERN = re.compile(r'^[a-zA-Z0-9_:\-]{1,64}$')


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
        if request.method == "GET" and hmac.compare_digest(api_key, API_KEY):
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


def get_request_key():
    """
    read the `key` query parameter and validate its format;
    reject unexpected characters to avoid redis key probing/injection
    :return: validated key or None
    """
    key = request.args.get('key')
    if key and not VALID_KEY_PATTERN.match(key):
        abort(400, description='invalid key parameter')
    return key


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
    can pass a `count` parameter to get multiple random proxies at once
    :return: get a random proxy
    """
    key = get_request_key()
    count = request.args.get('count', type=int)
    conn = get_conn()
    # return conn.random(key).string() if key else conn.random().string()
    if count and count > 1:
        # return multiple random proxies, one per line
        try:
            proxies = conn.randoms(count, key) if key else conn.randoms(count)
        except PoolEmptyException:
            if key and PROXY_RAND_KEY_DEGRADED:
                proxies = conn.randoms(count)
            else:
                raise
        return '\n'.join(proxy.string() for proxy in proxies)
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
    key = get_request_key()

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
    key = get_request_key()
    return str(conn.count(key)) if key else str(conn.count())


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
