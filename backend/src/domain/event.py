from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class CityEventType(StrEnum):
    VEHICLE_ENTERED_ROAD = "vehicle_entered_road"
    VEHICLE_REACHED_INTERSECTION = "vehicle_reached_intersection"
    TRAFFIC_LIGHT_CHANGED = "traffic_light_changed"
    EMERGENCY_DETECTED = "emergency_detected"
    TRAFFIC_INCIDENT = "traffic_incident"
    AGENT_DECISION_PROPOSED = "agent_decision_proposed"
    POLICY_REJECTED_ACTION = "policy_rejected_action"


@dataclass(frozen=True)
class CityEvent:
    id: UUID = field(default_factory=uuid4)
    event_type: CityEventType = CityEventType.TRAFFIC_INCIDENT
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    aggregate_id: UUID | None = None
    correlation_id: UUID = field(default_factory=uuid4)
    payload: dict[str, object] = field(default_factory=dict)