from cachetools import TTLCache


def get_cache(ttl_seconds: int = 1800, maxsize: int = 500) -> TTLCache:
    return TTLCache(maxsize=maxsize, ttl=ttl_seconds)
