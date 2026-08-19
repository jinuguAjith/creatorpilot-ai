"""Cost-control rate limiting (spec section 27): per-user daily generation
limits, on top of the credit system. Credits control *spend*; this limits
*request volume* so a compromised/scripted account can't hammer the
(expensive) generation endpoint even if it has a large credit balance.

In-memory sliding window here. Phase 13-real swaps this for Redis so
limits are enforced correctly across multiple backend instances — a
single-process in-memory counter under-counts once you scale horizontally.
"""
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.core.config import get_settings


class GenerationRateLimiter:
    def __init__(self):
        self._requests: dict[str, list[datetime]] = defaultdict(list)

    def check_and_record(self, user_id: str) -> None:
        settings = get_settings()
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(days=1)

        recent = [t for t in self._requests[user_id] if t > window_start]
        if len(recent) >= settings.max_generations_per_user_per_day:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Daily generation limit reached ({settings.max_generations_per_user_per_day}/day)",
            )
        recent.append(now)
        self._requests[user_id] = recent


_rate_limiter_singleton = GenerationRateLimiter()


def get_rate_limiter() -> GenerationRateLimiter:
    return _rate_limiter_singleton
