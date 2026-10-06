from enum import StrEnum
from uuid import UUID


class VehicleType(StrEnum):
    CAR = "car"
    BUS = "bus"
    EMERGENCY = "emergency"


class Vehicle:
    def __init__(
        self,
        vehicle_id: UUID,
        vehicle_type: VehicleType,
        latitude: float,
        longitude: float,
        speed_kmh: float = 0.0,
        road_id: UUID | None = None,
        position_on_road_meters: float = 0.0,
    ) -> None:
        self.id = vehicle_id
        self.type = vehicle_type
        self.latitude = latitude
        self.longitude = longitude
        self.speed_kmh = speed_kmh
        self.road_id = road_id
        self.position_on_road_meters = position_on_road_meters