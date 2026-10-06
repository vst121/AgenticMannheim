from dataclasses import dataclass
from uuid import UUID, uuid4

from domain.city import CityMetadata
from domain.intersection import Intersection, TrafficLightState
from domain.road import Road
from domain.vehicle import Vehicle, VehicleType


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

    def add_vehicle(
        self,
        vehicle_type: VehicleType,
        latitude: float,
        longitude: float,
        speed_kmh: float = 0.0,
        road_id: UUID | None = None,
        position_on_road_meters: float = 0.0,
    ) -> UUID:
        vehicle = Vehicle(
            vehicle_id=uuid4(),
            vehicle_type=vehicle_type,
            latitude=latitude,
            longitude=longitude,
            speed_kmh=speed_kmh,
            road_id=road_id,
            position_on_road_meters=position_on_road_meters,
        )

        self._state.vehicles.append(vehicle)

        return vehicle.id