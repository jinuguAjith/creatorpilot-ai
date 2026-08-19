from fastapi.testclient import TestClient

from app.main import app
from app.services.credit_service import get_credit_service

client = TestClient(app)


def _auth_headers():
    return {"Authorization": "Bearer dev-token"}


def test_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200


def test_create_campaign_without_auth_fails():
    resp = client.post("/v1/campaigns", json={
        "description": "test", "industry": "x", "style": "Modern",
        "target_audience": "x", "outputs": ["caption"],
    })
    assert resp.status_code == 401


def test_create_campaign_insufficient_credits():
    get_credit_service().set_balance("dev-user", 0)
    resp = client.post(
        "/v1/campaigns",
        headers=_auth_headers(),
        json={
            "description": "test campaign", "industry": "x", "style": "Modern",
            "target_audience": "x", "outputs": ["video"],
        },
    )
    assert resp.status_code == 402


def test_create_campaign_success():
    get_credit_service().set_balance("dev-user", 1000)
    resp = client.post(
        "/v1/campaigns",
        headers=_auth_headers(),
        json={
            "description": "Grand opening of Bella Aroma restaurant",
            "industry": "restaurant", "style": "Luxury",
            "target_audience": "couples and families", "outputs": ["poster", "caption"],
        },
    )
    assert resp.status_code == 202
    body = resp.json()
    assert body["status"] == "COMPLETED"

    job_id = body["job_id"]
    result = client.get(f"/v1/generations/{job_id}", headers=_auth_headers())
    assert result.status_code == 200
    assert result.json()["poster_url"] is not None
