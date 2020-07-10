import re

def parse_redis_connection_string(connection_string):
    """
    parse a redis connection string, for example:
    redis://[password]@host:port
    rediss://[password]@host:port
    :param connection_string:
    :return:
    """
    result = re.match('rediss?:\/\/(.*?)@(.*?):(\d+)\/(\d+)', connection_string)
    return result.group(2), int(result.group(3)), (result.group(1) or None), (result.group(4) or 0) if result \
        else ('localhost', 6379, None)
