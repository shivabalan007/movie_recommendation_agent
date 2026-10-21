import json
import logging
from typing import Any

from src.database.redis_connection import redis_client

logger = logging.getLogger(__name__)


def cache_get(key: str) -> Any | None:
    """Return cached JSON data, or None if missing/unavailable."""
    try:
        value = redis_client.get(key)

        if value is None:
            logger.info("CACHE MISS: %s", key)
            return None

        logger.info("CACHE HIT: %s", key)
        return json.loads(value)

    except Exception:
        logger.warning(
            "Redis cache read failed for key %s",
            key,
            exc_info=True,
        )
        return None


def cache_set(
    key: str,
    value: Any,
    ttl: int = 300,
) -> bool:
    """Cache JSON-serializable data for ttl seconds."""
    try:
        serialized = json.dumps(value, ensure_ascii=False)

        return bool(
            redis_client.set(
                key,
                serialized,
                ex=ttl,
            )
        )

    except (TypeError, ValueError):
        logger.warning(
            "Value for cache key %s is not JSON serializable",
            key,
            exc_info=True,
        )
        return False

    except Exception:
        logger.warning(
            "Redis cache write failed for key %s",
            key,
            exc_info=True,
        )
        return False


def cache_delete(key: str) -> bool:
    """Delete a cached value."""
    try:
        return redis_client.delete(key) > 0

    except Exception:
        logger.warning(
            "Redis cache delete failed for key %s",
            key,
            exc_info=True,
        )
        return False