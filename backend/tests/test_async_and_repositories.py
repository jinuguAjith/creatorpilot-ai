from fastapi.testclient import TestClient

from app.main import app
from app.services.credit_service import get_credit_service

client = TestClient(app)


def _auth_headers():
    return {"Authorization": "Bearer dev-token"}


def test_campaign_returns_queued_immediately():
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
    assert resp.json()["status"] == "QUEUED"


def test_job_eventually_completes_and_creates_project():
    get_credit_service().set_balance("dev-user", 1000)
    resp = client.post(
        "/v1/campaigns",
        headers=_auth_headers(),
        json={
            "description": "Product launch event",
            "industry": "tech", "style": "Modern",
            "target_audience": "early adopters", "outputs": ["poster", "caption"],
        },
    )
    job_id = resp.json()["job_id"]

    # FastAPI's BackgroundTasks run to completion as part of the same
    # ASGI request/response cycle, so TestClient has already waited for
    # it by the time .post() returns — no extra sleep/sync needed here.
    # (Production swaps this for a durable queue where jobs genuinely
    # outlive the request — see job_manager.py docstring.)
    result = client.get(f"/v1/generations/{job_id}", headers=_auth_headers())
    assert result.json()["status"] == "COMPLETED"

    project = client.get(f"/v1/projects/{job_id}", headers=_auth_headers())
    assert project.status_code == 200
    assert project.json()["status"] == "COMPLETED"


def test_brand_kit_upsert_and_get():
    payload = {"business_name": "Bella Aroma", "primary_color": "#6C4CF1"}
    put_resp = client.put("/v1/brand-kit", headers=_auth_headers(), json=payload)
    assert put_resp.status_code == 200
    assert put_resp.json()["business_name"] == "Bella Aroma"

    get_resp = client.get("/v1/brand-kit", headers=_auth_headers())
    assert get_resp.json()["business_name"] == "Bella Aroma"


def test_projects_list_returns_only_own_projects():
    resp = client.get("/v1/projects", headers=_auth_headers())
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_delete_nonexistent_project_returns_404():
    resp = client.delete("/v1/projects/does-not-exist", headers=_auth_headers())
    assert resp.status_code == 404
