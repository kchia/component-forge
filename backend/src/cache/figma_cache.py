"""Figma API response caching with metrics tracking."""

from typing import Optional
import time

from src.core.cache import BaseCache
from src.core.logging import get_logger

logger = get_logger(__name__)


class FigmaCache(BaseCache):
    """Cache for Figma API responses with hit rate tracking."""

    def __init__(self, ttl: int = 300):
        """
        Initialize Figma cache.

        Args:
            ttl: Time-to-live in seconds (default: 5 minutes)
        """
        super().__init__(ttl=ttl)
        self.cache_prefix = "figma:file"
        self.metrics_prefix = "figma:metrics"

    def _build_key(self, file_key: str, endpoint: str = "file") -> str:
        """
        Build cache key for Figma file.

        Args:
            file_key: Figma file key
            endpoint: API endpoint type (file, styles, etc.)

        Returns:
            Cache key string
        """
        return f"{self.cache_prefix}:{file_key}:{endpoint}"

    def _build_metrics_key(self, file_key: str, metric: str) -> str:
        """
        Build metrics key.

        Args:
            file_key: Figma file key
            metric: Metric type (hits, misses, latency)

        Returns:
            Metrics key string
        """
        return f"{self.metrics_prefix}:{file_key}:{metric}"

    async def get_file(self, file_key: str, endpoint: str = "file") -> Optional[dict]:
        """
        Get cached Figma file response.

        Args:
            file_key: Figma file key
            endpoint: API endpoint type

        Returns:
            Cached response or None (with _cached flag injected if found)
        """
        cache_key = self._build_key(file_key, endpoint)
        start_time = time.time()

        cached = await self.get(cache_key)

        # Track metrics
        latency = time.time() - start_time
        if cached:
            # Inject _cached flag to indicate this came from cache
            cached["_cached"] = True
            await self._track_hit(file_key, latency)
        else:
            await self._track_miss(file_key)

        return cached

    async def set_file(
        self, file_key: str, data: dict, endpoint: str = "file", ttl: Optional[int] = None
    ) -> bool:
        """
        Cache Figma file response.

        Args:
            file_key: Figma file key
            data: Response data to cache
            endpoint: API endpoint type
            ttl: Optional TTL override

        Returns:
            True if successful
        """
        cache_key = self._build_key(file_key, endpoint)
        return await self.set(cache_key, data, ttl)

    async def invalidate_file(self, file_key: str) -> int:
        """
        Invalidate all cache entries for a file.

        Args:
            file_key: Figma file key

        Returns:
            Number of keys deleted
        """
        pattern = f"{self.cache_prefix}:{file_key}:*"
        deleted = await self.delete_pattern(pattern)
        
        # Also clear metrics for this file
        await self._clear_metrics(file_key)
        
        logger.info(f"Invalidated cache for Figma file {file_key}: {deleted} keys")
        return deleted

    async def _track_hit(self, file_key: str, latency: float):
        """
        Track cache hit with latency.

        Args:
            file_key: Figma file key
            latency: Response latency in seconds
        """
        hits_key = self._build_metrics_key(file_key, "hits")
        latency_key = self._build_metrics_key(file_key, "latency")

        # Increment hit counter (1 hour TTL)
        await self.incr(hits_key, ttl=3600)

        # Track latency (simple moving average approach)
        # Store as milliseconds for better readability
        latency_ms = int(latency * 1000)
        if self.config.enabled:
            try:
                from src.core.cache import get_redis
                async with get_redis() as redis:
                    await redis.rpush(latency_key, str(latency_ms))
                    await redis.ltrim(latency_key, -100, -1)  # Keep last 100 samples
                    await redis.expire(latency_key, 3600)
            except Exception as e:
                logger.error(f"Error tracking latency: {e}")

    async def _track_miss(self, file_key: str):
        """
        Track cache miss.

        Args:
            file_key: Figma file key
        """
        misses_key = self._build_metrics_key(file_key, "misses")
        await self.incr(misses_key, ttl=3600)

    async def _clear_metrics(self, file_key: str):
        """
        Clear metrics for a file.

        Args:
            file_key: Figma file key
        """
        pattern = f"{self.metrics_prefix}:{file_key}:*"
        await self.delete_pattern(pattern)

    async def get_hit_rate(self, file_key: str) -> dict:
        """
        Get cache hit rate and metrics for a file.

        Args:
            file_key: Figma file key

        Returns:
            Dictionary with metrics
        """
        hits_key = self._build_metrics_key(file_key, "hits")
        misses_key = self._build_metrics_key(file_key, "misses")
        latency_key = self._build_metrics_key(file_key, "latency")

        hits = await self.get_int(hits_key) or 0
        misses = await self.get_int(misses_key) or 0
        total = hits + misses

        # Calculate average latency from samples
        avg_latency_ms = 0.0
        if self.config.enabled:
            try:
                from src.core.cache import get_redis
                async with get_redis() as redis:
                    latency_samples = await redis.lrange(latency_key, 0, -1)
                    if latency_samples:
                        avg_latency_ms = sum(int(s) for s in latency_samples) / len(latency_samples)
            except Exception as e:
                logger.error(f"Error calculating average latency: {e}")

        return {
            "file_key": file_key,
            "hits": hits,
            "misses": misses,
            "total_requests": total,
            "hit_rate": hits / total if total > 0 else 0.0,
            "avg_latency_ms": avg_latency_ms,
        }

    async def get_all_metrics(self) -> dict:
        """
        Get aggregated metrics across all files.

        Returns:
            Dictionary with aggregated metrics
        """
        # This would require scanning all metric keys
        # For now, return a simple structure
        # In production, consider using Redis streams or time-series DB
        return {
            "cache_enabled": self.config.enabled,
            "ttl_seconds": self.ttl,
            "message": "Use get_hit_rate(file_key) for per-file metrics",
        }
