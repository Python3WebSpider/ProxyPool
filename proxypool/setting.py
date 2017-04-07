# Redis数据库的地址和端口
HOST = 'localhost'
PORT = 6379

# 如果Redis有密码，则添加这句密码，否则设置为None
PASSWORD = 'foobared'

# 代理池数量界限
POOL_LOWER_THRESHOLD = 10
POOL_UPPER_THRESHOLD = 100

# 检查周期
VALID_CHECK_CYCLE = 60
POOL_LEN_CHECK_CYCLE = 20

# 测试API，用百度来测试
TEST_API='http://www.baidu.com'