import asyncio
import time
from typing import Any, Dict, Optional, Tuple

from src.leaky import fetch_root_hash


class CacheEntry:
    def __init__(self, data: Any, ttl: int, etag: Optional[str] = None):
        self.data = data
        self.ttl = ttl
        self.etag = etag
        self.created_at = time.time()
        self.last_checked = time.time()

    @property
    def expires_at(self) -> float:
        return self.created_at + self.ttl

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    def should_revalidate(self, stale_while_revalidate: int = 60) -> bool:
        """Check if entry should be revalidated (but can still be used)"""
        return time.time() > (self.expires_at - stale_while_revalidate)


class CacheStorage:
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
        self._root_hash: Optional[str] = None
        self._root_hash_ttl = 300  # 5 minutes
        self._last_root_check: float = 0
        self._leaky_base_url: Optional[str] = None

    def _get_lock(self, key: str) -> asyncio.Lock:
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    async def check_invalidation(self, base_url: str) -> bool:
        """Check if cache should be invalidated based on root hash"""
        self._leaky_base_url = base_url

        # Rate limit root hash checks
        now = time.time()
        if now - self._last_root_check < 10:  # Max once per 10 seconds
            return False

        self._last_root_check = now
        new_hash = await fetch_root_hash(self._leaky_base_url)

        if new_hash and self._root_hash and new_hash != self._root_hash:
            # Hash changed, invalidate all cache
            self._cache.clear()
            self._root_hash = new_hash
            return True

        if new_hash:
            self._root_hash = new_hash

        return False

    async def get(
        self,
        key: str,
        fetch_func=None,
        ttl: int = 3600,
        stale_while_revalidate: int = 60,
    ) -> Tuple[Any, bool]:
        """
        Get item from cache or fetch if needed.
        Returns (data, from_cache) tuple.
        """
        async with self._get_lock(key):
            entry = self._cache.get(key)

            # No entry or expired
            if not entry or entry.is_expired:
                if fetch_func:
                    data = await fetch_func()
                    self._cache[key] = CacheEntry(data, ttl)
                    return data, False
                return None, False

            # Entry exists and is fresh
            if not entry.should_revalidate(stale_while_revalidate):
                return entry.data, True

            # Entry should revalidate but can still be used
            # Start background revalidation
            if fetch_func:
                asyncio.create_task(self._background_revalidate(key, fetch_func, ttl))

            return entry.data, True

    async def _background_revalidate(self, key: str, fetch_func, ttl: int):
        """Background revalidation of stale entries"""
        try:
            async with self._get_lock(key):
                data = await fetch_func()
                self._cache[key] = CacheEntry(data, ttl)
        except Exception:
            # Silent fail - keep using stale data
            pass

    def set(self, key: str, data: Any, ttl: int = 3600):
        """Set item in cache"""
        self._cache[key] = CacheEntry(data, ttl)

    def invalidate(self, pattern: Optional[str] = None):
        """Invalidate cache entries matching pattern or all if None"""
        if pattern is None:
            self._cache.clear()
        else:
            keys_to_delete = [k for k in self._cache.keys() if pattern in k]
            for key in keys_to_delete:
                del self._cache[key]

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total = len(self._cache)
        expired = sum(1 for e in self._cache.values() if e.is_expired)
        stale = sum(1 for e in self._cache.values() if e.should_revalidate())

        return {
            "total_entries": total,
            "expired_entries": expired,
            "stale_entries": stale,
            "fresh_entries": total - expired - stale,
            "root_hash": self._root_hash,
        }


# Global cache instance
cache = CacheStorage()
