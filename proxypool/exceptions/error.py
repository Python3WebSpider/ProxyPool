class PoolEmptyException(Exception):
    def __str__(self):
        """
        proxypool is used out
        :return:
        """
        return repr('no proxy in proxypool')


class InvalidProxyException(Exception):
    def __str__(self):
        """
        proxy is invalid
        :return:
        """
        return repr('proxy is invalid')

