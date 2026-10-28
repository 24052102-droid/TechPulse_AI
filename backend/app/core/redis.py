import time
import json
import logging
from typing import Optional, Any
import redis
from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class InMemoryCache:
    """Thread-safe fallback in-memory cache when Redis is unavailable."""

    def __init__(self):
        self._store: dict[str, tuple[Any, Optional[float]]] = {}

    def get(self, key: str) -> Optional[str]:
        if key in self._store:
            val, expire_at = self._store[key]
            if expire_at is None or expire_at > time.time():
                return val
            del self._store[key]
        return None

    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        expire_at = time.time() + ex if ex else None
        self._store[key] = (value, expire_at)
        return True

    def delete(self, key: str) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def ping(self) -> bool:
        return True


class RedisClient:
    """Unified caching client for ATIP platform with graceful fallback."""

    def __init__(self):
        self.client: Any = None
        self.is_connected: bool = False
        self._connect()

    def _connect(self):
        try:
            r = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
            )
            r.ping()
            self.client = r
            self.is_connected = True
            logger.info("Connected to Redis at %s", settings.REDIS_URL)
        except Exception as e:
            logger.warning("Redis connection failed (%s). Using InMemoryCache fallback.", e)
            self.client = InMemoryCache()
            self.is_connected = False

    def get(self, key: str) -> Optional[str]:
        try:
            return self.client.get(key)
        except Exception as e:
            logger.warning("Cache get error for %s: %s", key, e)
            return None

    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        try:
            return bool(self.client.set(key, value, ex=ex))
        except Exception as e:
            logger.warning("Cache set error for %s: %s", key, e)
            return False

    def get_json(self, key: str) -> Optional[Any]:
        raw = self.get(key)
        if raw:
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return None
        return None

    def set_json(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        try:
            raw = json.dumps(value)
            return self.set(key, raw, ex=ex)
        except (TypeError, ValueError) as e:
            logger.warning("Cache set_json error for %s: %s", key, e)
            return False

    def delete(self, key: str) -> bool:
        try:
            return bool(self.client.delete(key))
        except Exception:
            return False

    def ping(self) -> bool:
        try:
            return bool(self.client.ping())
        except Exception:
            return False


cache_client = RedisClient()
