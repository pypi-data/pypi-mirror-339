from contextlib import contextmanager
from threading import Lock
from weakref import WeakValueDictionary


class BaseKey:
    def __init__(self, key: any = None):
        if type(self) is BaseKey:
            raise TypeError("BaseKey is an abstract class and cannot be instantiated directly.")
        self.key = key

    def __repr__(self):
        return f"{self.__class__.__module__}.{self.__class__.__name__}{f".{self.key}" if self.key is not None else ""}"

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, BaseKey):
            return self.__hash__() == other.__hash__()
        super().__eq__(other)


__lock_pool: WeakValueDictionary[BaseKey:Lock] = WeakValueDictionary()

__lock_global: Lock = Lock()


def __get_lock(key: BaseKey) -> Lock:
    with __lock_global:
        _lock: Lock | None = __lock_pool.get(key)
        if not _lock:
            _lock = Lock()
            __lock_pool[key] = _lock
        return _lock


@contextmanager
def lock(key: BaseKey):
    with __get_lock(key):
        yield
