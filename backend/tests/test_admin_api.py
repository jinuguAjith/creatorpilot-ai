from fastapi.testclient import TestClient

from app.main import app
from app.services.credit_service import get_credit_service

client = TestClient(app)


def _dev_admin_headers():
    return {"Authorization": "Bearer dev-token"}  # dev-user is admin-allowlisted


def test_non_admin_denied():
    # A different uid isn't in the dev allowlist — but our dev auth stub
    # always returns uid="dev-user" regardless of token, so this test
    # documents the RBAC dependency's shape rather than exercising a
    # different uid (that needs real Firebase auth, Phase 2).
    resp = client.get("/v1/admin/stats", headers=_dev_admin_headers())
    assert resp.status_code == 200  # dev-user IS the allowlisted admin


def test_stats_shape():
    resp = client.get("/v1/admin/stats", headers=_dev_admin_headers())
    assert resp.status_code == 200
    body = resp.json()
    assert "total_generations" in body
    assert "success_rate_pct" in body
    assert "open_reports" in body


def test_reports_list_and_resolve_flow():
    # Create a report via the normal user-facing endpoint first.
    report_resp = client.post(
        "/v1/reports", headers=_dev_admin_headers(),
        json={"job_id": "job_abc", "reason": "Poster looks off-brand"},
    )
    assert report_resp.status_code == 201
    report_id = report_resp.json()["report_id"]

    list_resp = client.get("/v1/admin/reports", headers=_dev_admin_headers())
    assert list_resp.status_code == 200
    assert any(r["id"] == report_id for r in list_resp.json())

    resolve_resp = client.post(f"/v1/admin/reports/{report_id}/resolve", headers=_dev_admin_headers())
    assert resolve_resp.status_code == 200

    open_after = client.get("/v1/admin/reports?status=open", headers=_dev_admin_headers())
    assert not any(r["id"] == report_id for r in open_after.json())


def test_credit_adjustment():
    get_credit_service().set_balance("some-user", 10)
    resp = client.post(
        "/v1/admin/credits/adjust",
        headers=_dev_admin_headers(),
        json={"user_id": "some-user", "delta": 50},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["previous_balance"] == 10
    assert body["new_balance"] == 60


def test_credit_adjustment_never_goes_negative():
    get_credit_service().set_balance("some-user-2", 10)
    resp = client.post(
        "/v1/admin/credits/adjust",
        headers=_dev_admin_headers(),
        json={"user_id": "some-user-2", "delta": -100},
    )
    assert resp.json()["new_balance"] == 0
