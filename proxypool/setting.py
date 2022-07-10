import platform
from os.path import dirname, abspath, join
from environs import Env
from loguru import logger
import shutil


env = Env()
env.read_env()

# definition of flags
IS_WINDOWS = platform.system().lower() == 'windows'

# definition of dirs
ROOT_DIR = dirname(dirname(abspath(__file__)))
LOG_DIR = join(ROOT_DIR, env.str('LOG_DIR', 'logs'))

# definition of environments
DEV_MODE, TEST_MODE, PROD_MODE = 'dev', 'test', 'prod'
APP_ENV = env.str('APP_ENV', DEV_MODE).lower()
APP_DEBUG = env.bool('APP_DEBUG', True if APP_ENV == DEV_MODE else False)
APP_DEV = IS_DEV = APP_ENV == DEV_MODE
APP_PROD = IS_PROD = APP_ENV == PROD_MODE
APP_TEST = IS_TEST = APP_ENV == TEST_MODE


# Which WSGI container is used to run applications
# - gevent: pip install gevent
# - tornado: pip install tornado
# - meinheld: pip install meinheld
APP_PROD_METHOD_GEVENT = 'gevent'
APP_PROD_METHOD_TORNADO = 'tornado'
APP_PROD_METHOD_MEINHELD = 'meinheld'
APP_PROD_METHOD = env.str('APP_PROD_METHOD', APP_PROD_METHOD_GEVENT).lower()

# redis host
REDIS_HOST = env.str('PROXYPOOL_REDIS_HOST',
                     env.str('REDIS_HOST', '127.0.0.1'))
# redis port
REDIS_PORT = env.int('PROXYPOOL_REDIS_PORT', env.int('REDIS_PORT', 6379))
# redis password, if no password, set it to None
REDIS_PASSWORD = env.str('PROXYPOOL_REDIS_PASSWORD',
                         env.str('REDIS_PASSWORD', None))
# redis db, if no choice, set it to 0
REDIS_DB = env.int('PROXYPOOL_REDIS_DB', env.int('REDIS_DB', 0))
# redis connection string, like redis://[password]@host:port or rediss://[password]@host:port/0,
# please refer to https://redis-py.readthedocs.io/en/stable/connections.html#redis.client.Redis.from_url
REDIS_CONNECTION_STRING = env.str(
    'PROXYPOOL_REDIS_CONNECTION_STRING', env.str('REDIS_CONNECTION_STRING', None))

# redis hash table key name
REDIS_KEY = env.str('PROXYPOOL_REDIS_KEY', env.str(
    'REDIS_KEY', 'proxies:universal'))

# definition of proxy scores
PROXY_SCORE_MAX = 100
PROXY_SCORE_MIN = 0
PROXY_SCORE_INIT = 10

# definition of proxy number
PROXY_NUMBER_MAX = 50000
PROXY_NUMBER_MIN = 0

# definition of tester cycle, it will test every CYCLE_TESTER second
CYCLE_TESTER = env.int('CYCLE_TESTER', 20)
# definition of getter cycle, it will get proxy every CYCLE_GETTER second
CYCLE_GETTER = env.int('CYCLE_GETTER', 100)
GET_TIMEOUT = env.int('GET_TIMEOUT', 10)

# definition of tester
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 10)
TEST_BATCH = env.int('TEST_BATCH', 20)
# only save anonymous proxy
TEST_ANONYMOUS = env.bool('TEST_ANONYMOUS', True)
# TEST_HEADERS = env.json('TEST_HEADERS', {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
# })
TEST_VALID_STATUS = env.list('TEST_VALID_STATUS', [200, 206, 302])

# definition of api
API_HOST = env.str('API_HOST', '0.0.0.0')
API_PORT = env.int('API_PORT', 5555)
API_THREADED = env.bool('API_THREADED', True)

# flags of enable
ENABLE_TESTER = env.bool('ENABLE_TESTER', True)
ENABLE_GETTER = env.bool('ENABLE_GETTER', True)
ENABLE_SERVER = env.bool('ENABLE_SERVER', True)


ENABLE_LOG_FILE = env.bool('ENABLE_LOG_FILE', True)
ENABLE_LOG_RUNTIME_FILE = env.bool('ENABLE_LOG_RUNTIME_FILE', True)
ENABLE_LOG_ERROR_FILE = env.bool('ENABLE_LOG_ERROR_FILE', True)


LOG_LEVEL_MAP = {
    DEV_MODE: "DEBUG",
    TEST_MODE: "INFO",
    PROD_MODE: "ERROR"
}

LOG_LEVEL = LOG_LEVEL_MAP.get(APP_ENV)
LOG_ROTATION = env.str('LOG_ROTATION', '500MB')
LOG_RETENTION = env.str('LOG_RETENTION', '1 week')

if ENABLE_LOG_FILE:
    if ENABLE_LOG_RUNTIME_FILE:
        logger.add(env.str('LOG_RUNTIME_FILE', join(LOG_DIR, 'runtime.log')),
                   level=LOG_LEVEL, rotation=LOG_ROTATION, retention=LOG_RETENTION)
    if ENABLE_LOG_ERROR_FILE:
        logger.add(env.str('LOG_ERROR_FILE', join(LOG_DIR, 'error.log')),
                   level='ERROR', rotation=LOG_ROTATION)
else:
    shutil.rmtree(LOG_DIR, ignore_errors=True)
