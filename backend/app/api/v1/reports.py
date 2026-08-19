import uuid

from fastapi import APIRouter, Depends

from app.core.auth import CurrentUser, get_current_user
from app.core.logging import get_logger
from app.repositories.report_repository import Report, ReportRepository, get_report_repository
from app.schemas.campaign import ReportRequest
from app.services.metrics_service import MetricsService, get_metrics_service

router = APIRouter(prefix="/v1", tags=["reports"])
logger = get_logger(__name__)


@router.post("/reports", status_code=201)
async def report_output(
    request: ReportRequest,
    user: CurrentUser = Depends(get_current_user),
    repo: ReportRepository = Depends(get_report_repository),
    metrics: MetricsService = Depends(get_metrics_service),
):
    report = Report(
        id=f"rep_{uuid.uuid4().hex[:10]}",
        job_id=request.job_id,
        reason=request.reason,
        reported_by=user.uid,
    )
    await repo.create(report)
    metrics.record_report()
    logger.info("ai_output_reported", job_id=request.job_id, reported_by=user.uid)
    return {"status": "received", "report_id": report.id}
