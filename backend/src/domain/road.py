from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class RoadType(StrEnum):
    RESIDENTIAL = "residential"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    SERVICE = "service"


@dataclass(frozen=True)
class Road:
    id: UUID
    name: str
    road_type: RoadType
    start_intersection_id: UUID
    end_intersection_id: UUID
    length_meters: float
    speed_limit_kmh: float
    lanes: int = 1