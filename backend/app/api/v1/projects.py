from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.auth import CurrentUser, get_current_user
from app.repositories.project_repository import Project, ProjectRepository, get_project_repository

router = APIRouter(prefix="/v1/projects", tags=["projects"])


class ProjectResponse(BaseModel):
    id: str
    campaign_title: str
    industry: str
    status: str
    poster_url: str | None
    video_url: str | None
    caption: str | None
    credits_consumed: int

    @classmethod
    def from_project(cls, p: Project) -> "ProjectResponse":
        return cls(
            id=p.id, campaign_title=p.campaign_title, industry=p.industry, status=p.status,
            poster_url=p.poster_url, video_url=p.video_url, caption=p.caption,
            credits_consumed=p.credits_consumed,
        )


@router.get("", response_model=list[ProjectResponse])
async def list_projects(
    user: CurrentUser = Depends(get_current_user),
    repo: ProjectRepository = Depends(get_project_repository),
):
    projects = await repo.list_for_user(user.uid)
    return [ProjectResponse.from_project(p) for p in projects]


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    user: CurrentUser = Depends(get_current_user),
    repo: ProjectRepository = Depends(get_project_repository),
):
    project = await repo.get(project_id, user.uid)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse.from_project(project)


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    user: CurrentUser = Depends(get_current_user),
    repo: ProjectRepository = Depends(get_project_repository),
):
    deleted = await repo.delete(project_id, user.uid)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
