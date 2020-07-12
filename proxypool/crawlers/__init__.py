import pkgutil
from .base import BaseCrawler
from .public.zhandaye import ZhandayeDetailCrawler
import inspect

# load classes subclass of BaseCrawler
PLUGINS = [
    "Daili66Crawler",
    "Data5UCrawler",
    "IP3366Crawler",
    "IPHaiCrawler",
    "KuaidailiCrawler",
    "XicidailiCrawler",
    "XiladailiCrawler",
    "ZhandayeCrawler",
    "TxtProxy"
]
classes = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)
    for name, value in inspect.getmembers(module):
        if inspect.isclass(value) and issubclass(value, BaseCrawler) and value is not BaseCrawler \
                and not getattr(value, 'ignore', False):
            if name not in PLUGINS:
                continue
            globals()[name] = value
            classes.append(value)
__all__ = __ALL__ = classes
print(__all__)