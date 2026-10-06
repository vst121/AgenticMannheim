from sqlalchemy.orm import Session

from digital_twin.twin import DigitalTwin, DigitalTwinState
from infrastructure.persistence.repositories.city_repository import CityRepository
from infrastructure.persistence.repositories.intersection_repository import (
    IntersectionRepository,
)
from infrastructure.persistence.repositories.road_repository import RoadRepository
from domain.vehicle import VehicleType


class DigitalTwinLoader:
    def __init__(self, session: Session) -> None:
        self._city_repository = CityRepository(session)
        self._intersection_repository = IntersectionRepository(session)
        self._road_repository = RoadRepository(session)

    def load(self) -> DigitalTwin:
        cities = self._city_repository.get_all()

        if not cities:
            raise RuntimeError("No city data found in the database.")

        city = cities[0]

        state = DigitalTwinState(
            city=city,
            roads=self._road_repository.get_all(),
            intersections=self._intersection_repository.get_all(),
            vehicles=[],
        )

        digital_twin = DigitalTwin(state)

        if state.intersections:
            intersection = state.intersections[0]

            digital_twin.add_vehicle(
                vehicle_type=VehicleType.EMERGENCY,
                latitude=intersection.latitude - 0.001,
                longitude=intersection.longitude,
                speed_kmh=40.0,
            )

        return digital_twin