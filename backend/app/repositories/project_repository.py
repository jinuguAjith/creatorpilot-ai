"""Repository pattern for `projects` (docs/DATABASE.md collection).
In-memory implementation here is used for dev/tests. Phase 8-real swaps in
FirestoreProjectRepository — same interface, so API routes never change.

Firestore collection shape (docs/DATABASE.md):
  projects/{projectId}: {
    user_id, campaign_title, input, industry, poster_url, video_url,
    caption, voiceover_url, status, credits_consumed, created_at
  }
Media files themselves live in Cloud Storage; only URLs are stored here,
per the spec's "do not store large media in Firestore" rule.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Project:
    id: str
    user_id: str
    campaign_title: str
    industry: str
    status: str
    poster_url: str | None = None
    video_url: str | None = None
    caption: str | None = None
    credits_consumed: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ProjectRepository(ABC):
    @abstractmethod
    async def create(self, project: Project) -> Project: ...

    @abstractmethod
    async def get(self, project_id: str, user_id: str) -> Project | None: ...

    @abstractmethod
    async def list_for_user(self, user_id: str, limit: int = 50) -> list[Project]: ...

    @abstractmethod
    async def delete(self, project_id: str, user_id: str) -> bool: ...

    @abstractmethod
    async def update_status(self, project_id: str, status: str, **fields) -> None: ...


class InMemoryProjectRepository(ProjectRepository):
    """Dev/test implementation. State resets on process restart — this is
    expected and fine until FirestoreProjectRepository lands."""

    def __init__(self):
        self._store: dict[str, Project] = {}

    async def create(self, project: Project) -> Project:
        self._store[project.id] = project
        return project

    async def get(self, project_id: str, user_id: str) -> Project | None:
        project = self._store.get(project_id)
        if project and project.user_id == user_id:
            return project
        return None  # never leak another user's project by ID guessing

    async def list_for_user(self, user_id: str, limit: int = 50) -> list[Project]:
        items = [p for p in self._store.values() if p.user_id == user_id]
        items.sort(key=lambda p: p.created_at, reverse=True)
        return items[:limit]

    async def delete(self, project_id: str, user_id: str) -> bool:
        project = await self.get(project_id, user_id)
        if not project:
            return False
        del self._store[project_id]
        return True

    async def update_status(self, project_id: str, status: str, **fields) -> None:
        project = self._store.get(project_id)
        if not project:
            return
        project.status = status
        for key, value in fields.items():
            if hasattr(project, key):
                setattr(project, key, value)


_project_repo_singleton = InMemoryProjectRepository()


def get_project_repository() -> ProjectRepository:
    return _project_repo_singleton
