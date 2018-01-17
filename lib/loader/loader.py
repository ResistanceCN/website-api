from functools import partial
from promise import Promise
from promise.dataloader import DataLoader
from expiringdict import ExpiringDict


class Loader(DataLoader):
    def __init__(self, timeout=None):
        DataLoader.__init__(self)

        self._timeout = timeout
        if timeout is not None:
            self._promise_cache_expiring = ExpiringDict(max_len=100, max_age_seconds=10)

    def _put_cached_promise(self, key, promise):
        if self._timeout is not None:
            self._promise_cache_expiring[key] = promise
        else:
            self._promise_cache[key] = promise

    def _get_cached_promise(self, key):
        if self._timeout is not None:
            return self._promise_cache_expiring.get(key)
        else:
            return self._promise_cache.get(key)

    def clear(self, key):
        cache_key = self.get_cache_key(key)

        if self._timeout is not None:
            self._promise_cache_expiring.pop(cache_key)
        else:
            self._promise_cache.pop(cache_key, None)

        return self

    def clear_all(self):
        if self._timeout is not None:
            self._promise_cache_expiring.clear()
        else:
            self._promise_cache = {}

        return self

    def load(self, key=None):
        if key is None:
            raise TypeError((
                'The loader.load() function must be called with a value,' +
                'but got: {}.'
            ).format(key))

        cache_key = self.get_cache_key(key)

        # If caching and there is a cache-hit, return cached Promise.
        if self.cache:
            cached_promise = self._get_cached_promise(cache_key)
            if cached_promise:
                return cached_promise

        # Otherwise, produce a new Promise for this value.
        promise = Promise(partial(self.do_resolve_reject, key))

        # If caching, cache this promise.
        if self.cache:
            self._put_cached_promise(cache_key, promise)

        return promise
