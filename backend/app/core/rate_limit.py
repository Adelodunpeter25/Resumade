from upstash_redis import Redis
from fastapi import Request, HTTPException, Depends
from app.core.config import settings
import time
from functools import wraps

redis = Redis(url=settings.upstash_redis_url, token=settings.upstash_redis_token)

RATE_LIMITS = {
    "default": "60/minute",
    "signup": "3/minute",
    "login": "3/minute",
    "forgot_password": "2/minute",
    "create_resume": "10/minute",
    "pdf_generate": "11/minute",
    "pdf_upload": "5/minute",
    "export": "10/minute",
    "ats_score": "5/minute",
}

class RateLimiter:
    def limit(self, limit_string: str):
        """Decorator for rate limiting endpoints"""
        max_requests, period = self._parse_limit(limit_string)
        window = self._get_window_seconds(period)
        
        def decorator(func):
            @wraps(func)
            async def async_wrapper(request: Request, *args, **kwargs):
                await self._check_rate_limit(request, max_requests, window)
                return await func(request, *args, **kwargs)
            
            @wraps(func)
            def sync_wrapper(request: Request, *args, **kwargs):
                self._check_rate_limit_sync(request, max_requests, window)
                return func(request, *args, **kwargs)
            
            # Return appropriate wrapper based on function type
            import asyncio
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper
        
        return decorator
    
    def _parse_limit(self, limit_string: str):
        """Parse '5/minute' into (5, 'minute')"""
        parts = limit_string.split("/")
        return int(parts[0]), parts[1]
    
    def _get_window_seconds(self, period: str):
        """Convert period to seconds"""
        periods = {"second": 1, "minute": 60, "hour": 3600, "day": 86400}
        return periods.get(period, 60)
    
    async def _check_rate_limit(self, request: Request, max_requests: int, window: int):
        """Async rate limit check"""
        self._check_rate_limit_sync(request, max_requests, window)
    
    def _check_rate_limit_sync(self, request: Request, max_requests: int, window: int):
        """Sync rate limit check using Upstash Redis"""
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}:{request.url.path}"
        
        current_time = int(time.time())
        window_start = current_time - window
        
        # Remove old entries
        redis.zremrangebyscore(key, 0, window_start)
        
        # Count requests in current window
        request_count = redis.zcard(key)
        
        if request_count >= max_requests:
            raise HTTPException(status_code=429, detail="Too many requests")
        
        # Add current request
        redis.zadd(key, {str(current_time): current_time})
        redis.expire(key, window)

limiter = RateLimiter()
