"""Aggregates the numbers the spec's admin dashboard (section 16) requires.
In-memory counters here; Phase 12-real swaps this for Firestore aggregation
queries or a proper analytics pipeline (e.g. BigQuery export) once volume
makes in-memory counting insufficient.
"""
from dataclasses import dataclass, field


@dataclass
class MetricsSnapshot:
    total_generations: int = 0
    successful_generations: int = 0
    failed_generations: int = 0
    credits_consumed: int = 0
    reports_count: int = 0


class MetricsService:
    def __init__(self):
        self._snapshot = MetricsSnapshot()

    def record_generation_success(self, credits_consumed: int) -> None:
        self._snapshot.total_generations += 1
        self._snapshot.successful_generations += 1
        self._snapshot.credits_consumed += credits_consumed

    def record_generation_failure(self) -> None:
        self._snapshot.total_generations += 1
        self._snapshot.failed_generations += 1

    def record_report(self) -> None:
        self._snapshot.reports_count += 1

    def snapshot(self) -> MetricsSnapshot:
        return self._snapshot


_metrics_singleton = MetricsService()


def get_metrics_service() -> MetricsService:
    return _metrics_singleton
