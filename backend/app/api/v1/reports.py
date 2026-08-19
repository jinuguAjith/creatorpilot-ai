from fastapi import APIRouter, Depends

from app.core.auth import CurrentUser, get_current_user
from app.core.logging import get_logger
from app.schemas.campaign import ReportRequest

router = APIRouter(prefix="/v1", tags=["reports"])
logger = get_logger(__name__)

# Phase 15 / 16: persist to Firestore `reports` collection and surface in
# the admin dashboard's report review queue.
_REPORTS: list[dict] = []


@router.post("/reports", status_code=201)
async def report_output(request: ReportRequest, user: CurrentUser = Depends(get_current_user)):
    entry = {"job_id": request.job_id, "reason": request.reason, "reported_by": user.uid}
    _REPORTS.append(entry)
    logger.info("ai_output_reported", job_id=request.job_id, reported_by=user.uid)
    return {"status": "received"}
