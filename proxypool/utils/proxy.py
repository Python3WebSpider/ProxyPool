from proxypool.schemas import Proxy


def is_valid_proxy(data):
    """
    check this string is within proxy format
    """
    if is_auth_proxy(data):
        host, port = extract_auth_proxy(data)
        return is_ip_valid(host) and is_port_valid(port)
    elif data.__contains__(':'):
        ip = data.split(':')[0]
        port = data.split(':')[1]
        return is_ip_valid(ip) and is_port_valid(port)
    else:
        return is_ip_valid(data)


def is_ip_valid(ip):
    """
    check this string is within ip format
    """
    if is_auth_proxy(ip):
        ip = ip.split('@')[1]
    a = ip.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def is_port_valid(port):
    return port.isdigit()


def convert_proxy_or_proxies(data):
    """
    convert list of str to valid proxies or proxy
    :param data:
    :return:
    """
    if not data:
        return None
    # if list of proxies
    if isinstance(data, list):
        result = []
        for item in data:
            # skip invalid item
            item = item.strip()
            if not is_valid_proxy(item): continue
            if is_auth_proxy(item):
                host, port = extract_auth_proxy(item)
            else:
                host, port = item.split(':')
            result.append(Proxy(host=host, port=int(port)))
        return result
    if isinstance(data, str) and is_valid_proxy(data):
        if is_auth_proxy(data):
            host, port = extract_auth_proxy(data)
        else:
            host, port = data.split(':')
        return Proxy(host=host, port=int(port))


def is_auth_proxy(data: str) -> bool:
    return '@' in data


def extract_auth_proxy(data: str) -> (str, str):
    """
    extract host and port from a proxy with authentication
    """
    auth = data.split('@')[0]
    ip_port = data.split('@')[1]
    ip = ip_port.split(':')[0]
    port = ip_port.split(':')[1]
    host = auth + '@' + ip
    return host, port


if __name__ == '__main__':
    proxy = 'test1234:test5678.@117.68.216.212:32425'
    print(extract_auth_proxy(proxy))
