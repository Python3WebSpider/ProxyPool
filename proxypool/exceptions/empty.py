class PoolEmptyException(Exception):
    def __str__(self):
        """
        proxyPool is used out
        :return:
        """
        return repr('no proxy in proxyPool')
