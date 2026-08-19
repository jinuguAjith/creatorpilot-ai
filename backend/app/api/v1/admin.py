"""Admin dashboard backend (spec section 16). Every route here requires
`require_admin` — never exposed to regular users. RBAC is enforced at the
dependency layer, not by hiding routes from docs, so an accidental
frontend link can never leak admin data.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.auth import CurrentUser
from app.core.credit_config import CreditConfig, DEFAULT_CREDIT_CONFIG, DEFAULT_PLANS
from app.core.rbac import require_admin
from app.repositories.report_repository import ReportRepository, get_report_repository
from app.services.credit_service import CreditService, get_credit_service
from app.services.metrics_service import MetricsService, get_metrics_service

router = APIRouter(prefix="/v1/admin", tags=["admin"])


class DashboardStats(BaseModel):
    total_generations: int
    successful_generations: int
    failed_generations: int
    success_rate_pct: float
    credits_consumed: int
    open_reports: int


class ReportSummary(BaseModel):
    id: str
    job_id: str
    reason: str
    reported_by: str
    status: str


class CreditAdjustment(BaseModel):
    user_id: str
    delta: int  # positive to grant, negative to deduct


@router.get("/stats", response_model=DashboardStats)
async def get_stats(
    admin: CurrentUser = Depends(require_admin),
    metrics: MetricsService = Depends(get_metrics_service),
    report_repo: ReportRepository = Depends(get_report_repository),
):
    snap = metrics.snapshot()
    success_rate = (
        (snap.successful_generations / snap.total_generations * 100) if snap.total_generations else 0.0
    )
    open_reports = await report_repo.list_all(status="open")
    return DashboardStats(
        total_generations=snap.total_generations,
        successful_generations=snap.successful_generations,
        failed_generations=snap.failed_generations,
        success_rate_pct=round(success_rate, 1),
        credits_consumed=snap.credits_consumed,
        open_reports=len(open_reports),
    )


@router.get("/reports", response_model=list[ReportSummary])
async def list_reports(
    status: str | None = None,
    admin: CurrentUser = Depends(require_admin),
    report_repo: ReportRepository = Depends(get_report_repository),
):
    reports = await report_repo.list_all(status=status)
    return [
        ReportSummary(id=r.id, job_id=r.job_id, reason=r.reason, reported_by=r.reported_by, status=r.status)
        for r in reports
    ]


@router.post("/reports/{report_id}/resolve")
async def resolve_report(
    report_id: str,
    admin: CurrentUser = Depends(require_admin),
    report_repo: ReportRepository = Depends(get_report_repository),
):
    updated = await report_repo.update_status(report_id, "reviewed")
    if not updated:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "resolved"}


@router.get("/credit-config", response_model=CreditConfig)
async def get_credit_config_admin(admin: CurrentUser = Depends(require_admin)):
    return DEFAULT_CREDIT_CONFIG


@router.get("/plans")
async def get_plans(admin: CurrentUser = Depends(require_admin)):
    return DEFAULT_PLANS


@router.post("/credits/adjust")
async def adjust_credits(
    adjustment: CreditAdjustment,
    admin: CurrentUser = Depends(require_admin),
    credit_service: CreditService = Depends(get_credit_service),
):
    # Manual admin grant/deduction — logged for audit purposes (structured
    # logging in credit_service already covers reserve/finalize/refund;
    # this path is separate since it bypasses the normal generation flow).
    current = credit_service.get_balance(adjustment.user_id)
    new_balance = max(0, current + adjustment.delta)
    credit_service.set_balance(adjustment.user_id, new_balance)
    return {"user_id": adjustment.user_id, "previous_balance": current, "new_balance": new_balance}
