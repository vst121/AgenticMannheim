from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class EvaluationOutcome(StrEnum):
    FAVORABLE = "favorable"
    UNFAVORABLE = "unfavorable"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True)
class EvaluationFinding:
    category: str
    description: str
    source: str
    confidence: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Finding confidence must be between 0 and 1.")


@dataclass
class InterventionEvaluation:
    proposal_id: UUID
    outcome: EvaluationOutcome = EvaluationOutcome.INCONCLUSIVE
    summary: str = ""
    findings: list[EvaluationFinding] = field(default_factory=list)
    expected_benefits: list[str] = field(default_factory=list)
    potential_risks: list[str] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    correlation_id: UUID = field(default_factory=uuid4)

    def add_finding(self, finding: EvaluationFinding) -> None:
        self.findings.append(finding)
