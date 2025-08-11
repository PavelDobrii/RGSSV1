"""Utilities for caching within the application."""

from cachetools import TTLCache


_cache: TTLCache | None = None


def get_cache(ttl_seconds: int = 1800, maxsize: int = 500) -> TTLCache:
    """Return a shared :class:`~cachetools.TTLCache` instance.

    The first call will create the cache and subsequent calls will return the
    same instance so that cached data can be reused across the application.
    Parameters allow configuring the cache on first use.
    """

    global _cache

    if _cache is None:
        _cache = TTLCache(maxsize=maxsize, ttl=ttl_seconds)

    return _cache
