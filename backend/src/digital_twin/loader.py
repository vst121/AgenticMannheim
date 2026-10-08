from sqlalchemy.orm import Session

from digital_twin.twin import DigitalTwin, DigitalTwinState
from domain.city import CityMetadata
from domain.vehicle import VehicleType
from infrastructure.persistence.repositories.city_repository import (
    CityRepository,
)
from infrastructure.persistence.repositories.intersection_repository import (
    IntersectionRepository,
)
from infrastructure.persistence.repositories.road_repository import (
    RoadRepository,
)


class DigitalTwinLoader:
    def __init__(self, session: Session) -> None:
        self._session = session

    def load(self) -> DigitalTwin:
        city_repository = CityRepository(self._session)
        intersection_repository = IntersectionRepository(self._session)
        road_repository = RoadRepository(self._session)

        city = city_repository.get_by_name("Mannheim")
        if city is None:
            raise ValueError("Mannheim was not found.")

        intersections = intersection_repository.get_all()
        roads = road_repository.get_all()

        if roads:
            print(
                "FIRST ROAD:",
                roads[0].name,
                roads[0].id,
                "geometry points:",
                len(roads[0].geometry),
                "first point:",
                roads[0].geometry[0]
                if roads[0].geometry
                else None,
            )

        print(
            f"Digital Twin loaded: "
            f"{len(intersections)} intersections, "
            f"{len(roads)} roads"
        )
        
        city_metadata = CityMetadata(
            name=city.name,
            area=city.area,
            latitude=city.latitude,
            longitude=city.longitude,
        )

        state = DigitalTwinState(
            city=city_metadata,
            roads=roads,
            intersections=intersections,
            vehicles=[],
        )

        twin = DigitalTwin(state)

        return twin