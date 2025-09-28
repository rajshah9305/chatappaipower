"""
Redis configuration and connection management
"""

import redis.asyncio as redis
from typing import Optional
import json
import asyncio

from app.core.config import settings

# Global Redis connection
_redis: Optional[redis.Redis] = None


async def init_redis():
    """Initialize Redis connection"""
    global _redis
    _redis = redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True
    )
    assert _redis is not None
    
    # Test connection
    try:
        await _redis.ping()
        print("Redis connection established")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise


async def get_redis() -> redis.Redis:
    """Get Redis connection"""
    global _redis
    if _redis is None:
        await init_redis()
    assert _redis is not None
    return _redis


async def close_redis():
    """Close Redis connection"""
    global _redis
    if _redis:
        await _redis.close()
        _redis = None


class RedisCache:
    """Redis cache utility class"""
    
    def __init__(self):
        self.redis = None
    
    async def initialize(self):
        """Initialize Redis connection"""
        self.redis = await get_redis()
    
    async def get(self, key: str) -> Optional[dict]:
        """Get value from cache"""
        if not self.redis:
            await self.initialize()
        assert self.redis is not None
        
        try:
            value = await self.redis.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"Error getting cache key {key}: {e}")
            return None
    
    async def set(self, key: str, value: dict, expire: int = 3600):
        """Set value in cache"""
        if not self.redis:
            await self.initialize()
        assert self.redis is not None
        
        try:
            await self.redis.setex(key, expire, json.dumps(value))
        except Exception as e:
            print(f"Error setting cache key {key}: {e}")
    
    async def delete(self, key: str):
        """Delete value from cache"""
        if not self.redis:
            await self.initialize()
        assert self.redis is not None
        
        try:
            await self.redis.delete(key)
        except Exception as e:
            print(f"Error deleting cache key {key}: {e}")
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.redis:
            await self.initialize()
        assert self.redis is not None
        
        try:
            return bool(await self.redis.exists(key))
        except Exception as e:
            print(f"Error checking cache key {key}: {e}")
            return False
    
    async def get_keys(self, pattern: str = "*") -> list:
        """Get all keys matching pattern"""
        if not self.redis:
            await self.initialize()
        assert self.redis is not None
        
        try:
            return await self.redis.keys(pattern)
        except Exception as e:
            print(f"Error getting keys with pattern {pattern}: {e}")
            return []


# Global cache instance
cache = RedisCache()