from enum import StrEnum
from uuid import UUID


class TrafficLightState(StrEnum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"


class Intersection:
    def __init__(
        self,
        intersection_id: UUID,
        name: str,
        latitude: float,
        longitude: float,
        traffic_light: TrafficLightState = TrafficLightState.RED,
    ) -> None:
        self.id = intersection_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.traffic_light = traffic_light