
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class InterventionType(StrEnum):
    TRAFFIC_CALMING = "traffic_calming"
    TRAFFIC_LIGHT_ADJUSTMENT = "traffic_light_adjustment"
    PEDESTRIAN_SAFETY = "pedestrian_safety"
    INFRASTRUCTURE_IMPROVEMENT = "infrastructure_improvement"
    FURTHER_INVESTIGATION = "further_investigation"


class InterventionStatus(StrEnum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    REJECTED = "rejected"
    EVALUATED = "evaluated"


@dataclass
class InterventionProposal:
    request_id: UUID
    investigation_id: UUID
    intervention_type: InterventionType
    title: str
    description: str
    expected_benefits: list[str] = field(default_factory=list)
    potential_risks: list[str] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    status: InterventionStatus = InterventionStatus.PROPOSED
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    correlation_id: UUID = field(default_factory=uuid4)

    def approve(self) -> None:
        self.status = InterventionStatus.APPROVED

    def reject(self) -> None:
        self.status = InterventionStatus.REJECTED

    def mark_evaluated(self) -> None:
        self.status = InterventionStatus.EVALUATED
