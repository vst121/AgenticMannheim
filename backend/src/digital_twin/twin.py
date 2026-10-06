from dataclasses import dataclass
from uuid import UUID

from domain.city import CityMetadata
from domain.intersection import Intersection, TrafficLightState
from domain.road import Road
from domain.vehicle import Vehicle


@dataclass
class DigitalTwinState:
    city: CityMetadata
    roads: list[Road]
    intersections: list[Intersection]
    vehicles: list[Vehicle]


class DigitalTwin:
    def __init__(self, state: DigitalTwinState) -> None:
        self._state = state

    def get_state(self) -> DigitalTwinState:
        return self._state

    def change_traffic_light(
        self,
        intersection_id: UUID,
        state: TrafficLightState,
    ) -> None:
        intersection = next(
            (
                intersection
                for intersection in self._state.intersections
                if intersection.id == intersection_id
            ),
            None,
        )

        if intersection is None:
            raise ValueError(
                f"Intersection '{intersection_id}' was not found."
            )

        intersection.traffic_light = state