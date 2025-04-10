from asyncio import Lock
from contextlib import asynccontextmanager
from weakref import WeakValueDictionary

from .base_key import BaseKey

__lock_pool: WeakValueDictionary[BaseKey:Lock] = WeakValueDictionary()

__lock_global: Lock = Lock()


async def get_lock(key: BaseKey) -> Lock:
    async with __lock_global:
        _lock: Lock | None = __lock_pool.get(key)
        if not _lock:
            _lock = Lock()
            __lock_pool[key] = _lock
        return _lock


@asynccontextmanager
async def lock(key: BaseKey):
    _lock = await  get_lock(key)
    async with _lock:
        yield
