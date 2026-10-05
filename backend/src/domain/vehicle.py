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
    ) -> None:
        self.id = vehicle_id
        self.type = vehicle_type
        self.latitude = latitude
        self.longitude = longitude
        self.speed_kmh = speed_kmh