from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class SimulationActionType(StrEnum):
    CHANGE_TRAFFIC_LIGHT = "change_traffic_light"


@dataclass(frozen=True)
class SimulationAction:
    action_type: SimulationActionType
    intersection_id: UUID
    traffic_light_state: str
    vehicle_id: UUID