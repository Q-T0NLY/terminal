"""
⚡ Shared Caching Layer
Production-grade caching with Redis
"""

import redis
import json
from typing import Optional, Any
from datetime import timedelta
import os
import hashlib
import pickle

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=False)
    redis_client.ping()
    REDIS_AVAILABLE = True
except:
    REDIS_AVAILABLE = False
    redis_client = None


class Cache:
    """Cache manager with Redis backend"""
    
    DEFAULT_TTL = 300  # 5 minutes
    
    @staticmethod
    def _make_key(prefix: str, key: str) -> str:
        """Generate cache key"""
        return f"ose:{prefix}:{key}"
    
    @staticmethod
    def get(prefix: str, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not REDIS_AVAILABLE:
            return None
        
        try:
            cache_key = Cache._make_key(prefix, key)
            value = redis_client.get(cache_key)
            if value:
                return pickle.loads(value)
        except Exception:
            pass
        return None
    
    @staticmethod
    def set(prefix: str, key: str, value: Any, ttl: int = DEFAULT_TTL):
        """Set value in cache"""
        if not REDIS_AVAILABLE:
            return
        
        try:
            cache_key = Cache._make_key(prefix, key)
            redis_client.setex(
                cache_key,
                ttl,
                pickle.dumps(value)
            )
        except Exception:
            pass
    
    @staticmethod
    def delete(prefix: str, key: str):
        """Delete value from cache"""
        if not REDIS_AVAILABLE:
            return
        
        try:
            cache_key = Cache._make_key(prefix, key)
            redis_client.delete(cache_key)
        except Exception:
            pass
    
    @staticmethod
    def clear_prefix(prefix: str):
        """Clear all keys with prefix"""
        if not REDIS_AVAILABLE:
            return
        
        try:
            pattern = f"ose:{prefix}:*"
            for key in redis_client.scan_iter(match=pattern):
                redis_client.delete(key)
        except Exception:
            pass
    
    @staticmethod
    def cached(prefix: str, ttl: int = DEFAULT_TTL):
        """Decorator for caching function results"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Generate cache key from function args
                key_data = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                key = hashlib.md5(key_data.encode()).hexdigest()
                
                # Try to get from cache
                cached_value = Cache.get(prefix, key)
                if cached_value is not None:
                    return cached_value
                
                # Call function and cache result
                result = func(*args, **kwargs)
                Cache.set(prefix, key, result, ttl)
                return result
            return wrapper
        return decorator


# Convenience functions for common caching patterns

def cache_scan_result(scan_id: str, result: dict, ttl: int = 3600):
    """Cache scan result"""
    Cache.set("scan", scan_id, result, ttl)


def get_cached_scan(scan_id: str) -> Optional[dict]:
    """Get cached scan result"""
    return Cache.get("scan", scan_id)


def cache_optimization_result(task_id: str, result: dict, ttl: int = 1800):
    """Cache optimization result"""
    Cache.set("optimization", task_id, result, ttl)


def get_cached_optimization(task_id: str) -> Optional[dict]:
    """Get cached optimization result"""
    return Cache.get("optimization", task_id)
