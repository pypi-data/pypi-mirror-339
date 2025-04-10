from contextlib import contextmanager
from threading import Lock
from weakref import WeakValueDictionary

from .base_key import BaseKey

__lock_pool: WeakValueDictionary[BaseKey:Lock] = WeakValueDictionary()

__lock_global: Lock = Lock()
__last_lock: Lock


def get_lock(key: BaseKey) -> Lock:
    global __last_lock
    with __lock_global:
        _lock: Lock | None = __lock_pool.get(key)
        if not _lock:
            _lock = Lock()
            __lock_pool[key] = _lock
        __last_lock = _lock
        return _lock


@contextmanager
def lock(key: BaseKey):
    _lock = get_lock(key)
    with _lock:
        yield
