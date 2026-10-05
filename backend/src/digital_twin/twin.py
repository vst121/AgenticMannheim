from dataclasses import asdict, dataclass
from uuid import UUID

from domain.city import CityMetadata
from domain.intersection import Intersection
from domain.vehicle import Vehicle


@dataclass
class DigitalTwinState:
    city: CityMetadata
    vehicles: list[Vehicle]
    intersections: list[Intersection]


class DigitalTwin:
    def __init__(self) -> None:
        self._state = DigitalTwinState(
            city=CityMetadata(
                name="Mannheim",
                area="Innenstadt",
                latitude=49.4875,
                longitude=8.4660,
            ),
            vehicles=[],
            intersections=[],
        )

    def get_state(self) -> DigitalTwinState:
        return self._state