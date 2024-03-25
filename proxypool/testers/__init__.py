import pkgutil
from .base import BaseTester
import inspect


# load classes subclass of BaseCrawler
classes = []
for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)
    for name, value in inspect.getmembers(module):
        globals()[name] = value
        if inspect.isclass(value) and issubclass(value, BaseTester) and value is not BaseTester \
                and not getattr(value, 'ignore', False):
            classes.append(value)
__all__ = __ALL__ = classes

