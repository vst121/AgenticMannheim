
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class InvestigationStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class InvestigationFinding:
    category: str
    description: str
    source: str
    confidence: float


@dataclass
class Investigation:
    request_id: UUID
    findings: list[InvestigationFinding] = field(default_factory=list)
    related_request_ids: list[UUID] = field(default_factory=list)
    related_event_ids: list[UUID] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    status: InvestigationStatus = InvestigationStatus.COMPLETED
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    correlation_id: UUID = field(default_factory=uuid4)

    def add_finding(self, finding: InvestigationFinding) -> None:
        if not 0.0 <= finding.confidence <= 1.0:
            raise ValueError("Finding confidence must be between 0 and 1.")
        self.findings.append(finding)

    def mark_failed(self) -> None:
        self.status = InvestigationStatus.FAILED
