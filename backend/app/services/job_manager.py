"""Phase 6: campaigns no longer block on generation. The endpoint enqueues
a job and returns immediately with status=QUEUED; a background task walks
it through PROCESSING -> GENERATING -> COMPOSING -> COMPLETED/FAILED.

This in-process background-task version is a stepping stone: real
production traffic needs a durable queue (Cloud Tasks/Celery/Pub-Sub) so
jobs survive a server restart and can be retried with backoff. That swap
happens behind `enqueue()` without changing API routes.
"""
from fastapi import BackgroundTasks

from app.core.credit_config import get_credit_config
from app.core.logging import get_logger
from app.repositories.project_repository import Project, ProjectRepository
from app.schemas.campaign import CampaignRequest, GenerationResultResponse, GenerationStatus
from app.services.credit_service import CreditService
from app.services.orchestrator import ContentModerationError, Orchestrator

logger = get_logger(__name__)


class JobManager:
    def __init__(self):
        # Phase 8/production: back this with Firestore `generations` docs
        # instead of an in-memory dict, so status survives restarts and is
        # queryable from the mobile app / admin dashboard directly.
        self._jobs: dict[str, GenerationResultResponse] = {}

    def get(self, job_id: str) -> GenerationResultResponse | None:
        return self._jobs.get(job_id)

    def _set_status(self, job_id: str, status: GenerationStatus, **fields):
        current = self._jobs.get(job_id) or GenerationResultResponse(job_id=job_id, status=status)
        updated = current.model_copy(update={"status": status, **fields})
        self._jobs[job_id] = updated

    async def enqueue(
        self,
        background_tasks: BackgroundTasks,
        job_id: str,
        user_id: str,
        request: CampaignRequest,
        orchestrator: Orchestrator,
        credit_service: CreditService,
        project_repository: ProjectRepository,
        credits_reserved: int,
    ) -> None:
        self._set_status(job_id, GenerationStatus.queued)
        # Real deployment: this becomes a Cloud Tasks / Celery enqueue call
        # instead of FastAPI BackgroundTasks, so processing survives a
        # server restart and can be retried with backoff across machines.
        background_tasks.add_task(
            self._process, job_id, user_id, request, orchestrator, credit_service, project_repository, credits_reserved
        )

    async def _process(
        self,
        job_id: str,
        user_id: str,
        request: CampaignRequest,
        orchestrator: Orchestrator,
        credit_service: CreditService,
        project_repository: ProjectRepository,
        credits_reserved: int,
    ) -> None:
        try:
            self._set_status(job_id, GenerationStatus.processing)
            self._set_status(job_id, GenerationStatus.generating)

            result = await orchestrator.run(job_id, request)

            self._set_status(job_id, GenerationStatus.composing)
            credit_service.finalize(job_id)

            await project_repository.create(
                Project(
                    id=job_id,
                    user_id=user_id,
                    campaign_title=request.description[:60],
                    industry=request.industry,
                    status=GenerationStatus.completed.value,
                    poster_url=result.poster_url,
                    video_url=result.video_url,
                    caption=result.caption,
                    credits_consumed=credits_reserved,
                )
            )
            self._set_status(
                job_id,
                GenerationStatus.completed,
                poster_url=result.poster_url,
                video_url=result.video_url,
                caption=result.caption,
                hashtags=result.hashtags,
                cta=result.cta,
            )
            logger.info("job_completed", job_id=job_id)

        except ContentModerationError as exc:
            credit_service.refund(job_id)
            self._set_status(job_id, GenerationStatus.failed, error_message=str(exc))
            logger.warning("job_failed_moderation", job_id=job_id)

        except Exception as exc:  # noqa: BLE001 — any failure refunds credits
            credit_service.refund(job_id)
            self._set_status(job_id, GenerationStatus.failed, error_message="Generation failed")
            logger.error("job_failed", job_id=job_id, error=str(exc))


_job_manager_singleton = JobManager()


def get_job_manager() -> JobManager:
    return _job_manager_singleton
