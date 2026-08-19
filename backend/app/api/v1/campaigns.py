import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import CurrentUser, get_current_user
from app.core.dependencies import get_orchestrator
from app.core.logging import get_logger
from app.schemas.campaign import (
    CampaignJobResponse,
    CampaignRequest,
    GenerationResultResponse,
    GenerationStatus,
)
from app.services.credit_service import CreditService, InsufficientCreditsError, get_credit_service
from app.services.orchestrator import ContentModerationError, Orchestrator

router = APIRouter(prefix="/v1", tags=["campaigns"])
logger = get_logger(__name__)

# Phase 8: replace with Firestore `generations` collection.
_JOB_RESULTS: dict[str, GenerationResultResponse] = {}


@router.post("/campaigns", response_model=CampaignJobResponse, status_code=202)
async def create_campaign(
    request: CampaignRequest,
    user: CurrentUser = Depends(get_current_user),
    credit_service: CreditService = Depends(get_credit_service),
    orchestrator: Orchestrator = Depends(get_orchestrator),
):
    job_id = f"job_{uuid.uuid4().hex[:10]}"
    cost = credit_service.cost_for_outputs([o.value for o in request.outputs])

    try:
        credit_service.reserve(user.uid, reservation_id=job_id, amount=cost)
    except InsufficientCreditsError as exc:
        raise HTTPException(status_code=402, detail=str(exc)) from exc

    try:
        # Phase 6: this should enqueue an async job (Celery/Cloud Tasks)
        # rather than run inline, so the endpoint returns immediately and
        # a worker processes generation with retry/timeout/concurrency
        # limits per docs/AI_WORKFLOW.md. Running inline here for the
        # Phase 4 milestone (mocked, synchronous, fast).
        result = await orchestrator.run(job_id, request)
        credit_service.finalize(job_id)
        _JOB_RESULTS[job_id] = result
    except ContentModerationError as exc:
        credit_service.refund(job_id)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001 — refund on ANY failure, then re-raise
        credit_service.refund(job_id)
        logger.error("generation_failed", job_id=job_id, error=str(exc))
        _JOB_RESULTS[job_id] = GenerationResultResponse(
            job_id=job_id, status=GenerationStatus.failed, error_message="Generation failed"
        )
        raise HTTPException(status_code=500, detail="Generation failed, credits refunded") from exc

    return CampaignJobResponse(job_id=job_id, status=GenerationStatus.completed, credits_reserved=cost)


@router.get("/generations/{job_id}", response_model=GenerationResultResponse)
async def get_generation(job_id: str, user: CurrentUser = Depends(get_current_user)):
    result = _JOB_RESULTS.get(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return result
