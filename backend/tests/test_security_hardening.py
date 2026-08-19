from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.core.rate_limit import GenerationRateLimiter
from app.main import app
from app.services.credit_service import get_credit_service

client = TestClient(app)


def _auth_headers():
    return {"Authorization": "Bearer dev-token"}


def test_security_headers_present():
    resp = client.get("/healthz")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"


def test_oversized_description_rejected():
    get_credit_service().set_balance("dev-user", 1000)
    resp = client.post(
        "/v1/campaigns",
        headers=_auth_headers(),
        json={
            "description": "x" * 5000,  # exceeds 2000 char limit
            "industry": "restaurant", "style": "Luxury",
            "target_audience": "families", "outputs": ["caption"],
        },
    )
    assert resp.status_code == 422


def test_empty_outputs_rejected():
    get_credit_service().set_balance("dev-user", 1000)
    resp = client.post(
        "/v1/campaigns",
        headers=_auth_headers(),
        json={
            "description": "test", "industry": "x", "style": "Modern",
            "target_audience": "x", "outputs": [],
        },
    )
    assert resp.status_code == 422


def test_duplicate_outputs_rejected():
    get_credit_service().set_balance("dev-user", 1000)
    resp = client.post(
        "/v1/campaigns",
        headers=_auth_headers(),
        json={
            "description": "test", "industry": "x", "style": "Modern",
            "target_audience": "x", "outputs": ["poster", "poster"],
        },
    )
    assert resp.status_code == 422


def test_rate_limiter_blocks_after_daily_limit():
    from fastapi import HTTPException

    limiter = GenerationRateLimiter()
    limit = get_settings().max_generations_per_user_per_day
    for _ in range(limit):
        limiter.check_and_record("rate-test-user")

    raised = False
    try:
        limiter.check_and_record("rate-test-user")
    except HTTPException as exc:
        raised = True
        assert exc.status_code == 429
    assert raised, "expected HTTPException(429) once daily limit is exceeded"


def test_rate_limiter_is_per_user():
    limiter = GenerationRateLimiter()
    limit = get_settings().max_generations_per_user_per_day
    for _ in range(limit):
        limiter.check_and_record("user-a")
    # user-b has its own independent window — must not be blocked
    limiter.check_and_record("user-b")
