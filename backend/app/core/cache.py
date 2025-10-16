import redis
import json
import hashlib
from functools import wraps
from typing import Any, Optional
from app.core.config import settings
from app.core.constants import CacheConstants
import logging

logger = logging.getLogger(__name__)

def serialize_for_cache(obj):
    """Serialize objects for Redis cache"""
    if hasattr(obj, '__dict__'):
        # SQLAlchemy model or similar object
        return {
            '_type': obj.__class__.__name__,
            '_data': {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        }
    return obj

def deserialize_from_cache(data):
    """Deserialize objects from Redis cache"""
    if isinstance(data, dict) and '_type' in data:
        # This is a serialized object - return as dict for now
        # In production, you might want to reconstruct the actual object
        return data['_data']
    return data

class RedisCache:
    def __init__(self):
        self.client = None
        self._connect()
    
    def _connect(self):
        """Connect to Upstash Redis"""
        try:
            self.client = redis.Redis(
                host=settings.upstash_redis_url.replace('https://', '').replace('http://', ''),
                port=6379,
                password=settings.upstash_redis_token,
                ssl=True,
                decode_responses=True
            )
            # Test connection
            self.client.ping()
            logger.info("Connected to Upstash Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.client:
            return None
        try:
            value = self.client.get(key)
            if value:
                data = json.loads(value)
                return deserialize_from_cache(data)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = CacheConstants.TEMPLATE_CACHE_TTL):
        """Set value in cache with TTL"""
        if not self.client:
            return False
        try:
            serialized_value = serialize_for_cache(value)
            self.client.setex(key, ttl, json.dumps(serialized_value))
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False
    
    def delete(self, key: str):
        """Delete key from cache"""
        if not self.client:
            return False
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False

    def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        if not self.client:
            return False
        try:
            keys = self.client.keys(f"*{pattern}*")
            if keys:
                self.client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Redis clear pattern error: {e}")
            return False
    
    def clear_all(self):
        """Clear all cache (use with caution)"""
        if not self.client:
            return False
        try:
            self.client.flushdb()
            return True
        except Exception as e:
            logger.error(f"Redis clear all error: {e}")
            return False

# Global Redis cache instance
redis_cache = RedisCache()

# Cache management utilities
def clear_user_cache(user_id: int):
    """Clear cache for specific user"""
    redis_cache.clear_pattern(f"*user*{user_id}*")

def clear_resume_cache(resume_id: int):
    """Clear cache for specific resume"""
    redis_cache.clear_pattern(f"*resume*{resume_id}*")

def clear_template_cache():
    """Clear template cache"""
    redis_cache.clear_pattern("*template*")

def cache_key(*args, **kwargs):
    """Generate cache key from arguments"""
    safe_args = [str(arg) for arg in args[1:]] if args and hasattr(args[0], '__dict__') else [str(arg) for arg in args]
    safe_kwargs = {k: str(v) for k, v in kwargs.items()}
    key_data = json.dumps({"args": safe_args, "kwargs": safe_kwargs}, sort_keys=True)
    return hashlib.md5(key_data.encode()).hexdigest()

def cached(ttl: int = CacheConstants.TEMPLATE_CACHE_TTL):
    """Decorator for caching function results in Redis"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            result = redis_cache.get(key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            redis_cache.set(key, result, ttl)
            return result
        return wrapper
    return decorator

# Backward compatibility
template_cache = redis_cache
