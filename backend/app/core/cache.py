from cachetools import TTLCache
from functools import wraps
import hashlib
import json
from app.core.constants import CacheConstants

# In-memory cache for templates
template_cache = TTLCache(maxsize=CacheConstants.TEMPLATE_CACHE_SIZE, ttl=CacheConstants.TEMPLATE_CACHE_TTL)

def cache_key(*args, **kwargs):
    """Generate cache key from arguments"""
    # Convert args to strings, skip first arg if it's self/cls
    safe_args = [str(arg) for arg in args[1:]] if args and hasattr(args[0], '__dict__') else [str(arg) for arg in args]
    safe_kwargs = {k: str(v) for k, v in kwargs.items()}
    key_data = json.dumps({"args": safe_args, "kwargs": safe_kwargs}, sort_keys=True)
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
