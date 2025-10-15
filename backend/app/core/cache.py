from cachetools import TTLCache
from functools import wraps
import hashlib
import json

# In-memory cache with 1 hour TTL, max 100 items
template_cache = TTLCache(maxsize=100, ttl=3600)

def cache_key(*args, **kwargs):
    """Generate cache key from arguments"""
    key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
    return hashlib.md5(key_data.encode()).hexdigest()

def cached(cache):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = cache_key(*args, **kwargs)
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper
    return decorator
