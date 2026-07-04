from loguru import logger

# geolite2 provides an offline IP -> country database (bundled with the
# maxminddb_geolite2 dependency). loading it can fail if the optional
# dependency is missing, so degrade gracefully and disable area filtering.
try:
    from geolite2 import geolite2

    _reader = geolite2.reader()
except Exception as e:  # pragma: no cover
    _reader = None
    logger.warning(f'geolite2 is unavailable, area filtering disabled: {e}')


def get_country_iso(ip):
    """
    look up the ISO country code (e.g. 'CN', 'US') for an ip address
    :param ip: ip address string
    :return: uppercase iso code, or None if unknown/unavailable
    """
    if _reader is None:
        return None
    try:
        record = _reader.get(ip)
    except Exception:
        return None
    if not record:
        return None
    country = record.get('country') or record.get('registered_country') or {}
    return country.get('iso_code')


if __name__ == '__main__':
    print('8.8.8.8', get_country_iso('8.8.8.8'))
    print('114.114.114.114', get_country_iso('114.114.114.114'))
