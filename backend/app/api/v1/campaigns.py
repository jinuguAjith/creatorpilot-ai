import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from app.core.auth import CurrentUser, get_current_user
from app.core.dependencies import get_orchestrator
from app.core.logging import get_logger
from app.repositories.project_repository import ProjectRepository, get_project_repository
from app.schemas.campaign import (
    CampaignJobResponse,
    CampaignRequest,
    GenerationResultResponse,
    GenerationStatus,
)
from app.services.credit_service import CreditService, InsufficientCreditsError, get_credit_service
from app.services.job_manager import JobManager, get_job_manager
from app.services.orchestrator import Orchestrator

router = APIRouter(prefix="/v1", tags=["campaigns"])
logger = get_logger(__name__)


@router.post("/campaigns", response_model=CampaignJobResponse, status_code=202)
async def create_campaign(
    request: CampaignRequest,
    background_tasks: BackgroundTasks,
    user: CurrentUser = Depends(get_current_user),
    credit_service: CreditService = Depends(get_credit_service),
    orchestrator: Orchestrator = Depends(get_orchestrator),
    job_manager: JobManager = Depends(get_job_manager),
    project_repository: ProjectRepository = Depends(get_project_repository),
):
    job_id = f"job_{uuid.uuid4().hex[:10]}"
    cost = credit_service.cost_for_outputs([o.value for o in request.outputs])

    try:
        credit_service.reserve(user.uid, reservation_id=job_id, amount=cost)
    except InsufficientCreditsError as exc:
        raise HTTPException(status_code=402, detail=str(exc)) from exc

    # Returns immediately with QUEUED — mobile app polls / will later
    # receive an FCM push on completion (Phase 6 follow-up).
    await job_manager.enqueue(
        background_tasks, job_id, user.uid, request, orchestrator, credit_service, project_repository, cost
    )

    return CampaignJobResponse(job_id=job_id, status=GenerationStatus.queued, credits_reserved=cost)


@router.get("/generations/{job_id}", response_model=GenerationResultResponse)
async def get_generation(
    job_id: str,
    user: CurrentUser = Depends(get_current_user),
    job_manager: JobManager = Depends(get_job_manager),
):
    result = job_manager.get(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return result
