from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class AgentDecisionType(StrEnum):
    PRIORITIZE_EMERGENCY = "prioritize_emergency"


@dataclass(frozen=True)
class AgentDecision:
    decision_type: AgentDecisionType
    intersection_id: UUID
    reason: str
    vehicle_id: UUID