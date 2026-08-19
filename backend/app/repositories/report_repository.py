"""Repository for `reports/{reportId}` (spec section 15/16: users can flag
AI output, admin reviews the queue).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class Report:
    id: str
    job_id: str
    reason: str
    reported_by: str
    status: str = "open"  # open | reviewed | dismissed
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ReportRepository(ABC):
    @abstractmethod
    async def create(self, report: Report) -> Report: ...

    @abstractmethod
    async def list_all(self, status: str | None = None) -> list[Report]: ...

    @abstractmethod
    async def update_status(self, report_id: str, status: str) -> bool: ...


class InMemoryReportRepository(ReportRepository):
    def __init__(self):
        self._store: dict[str, Report] = {}

    async def create(self, report: Report) -> Report:
        self._store[report.id] = report
        return report

    async def list_all(self, status: str | None = None) -> list[Report]:
        items = list(self._store.values())
        if status:
            items = [r for r in items if r.status == status]
        items.sort(key=lambda r: r.created_at, reverse=True)
        return items

    async def update_status(self, report_id: str, status: str) -> bool:
        report = self._store.get(report_id)
        if not report:
            return False
        report.status = status
        return True


_report_repo_singleton = InMemoryReportRepository()


def get_report_repository() -> ReportRepository:
    return _report_repo_singleton
