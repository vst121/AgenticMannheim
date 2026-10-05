from dataclasses import dataclass


@dataclass(frozen=True)
class CityMetadata:
    name: str
    area: str
    latitude: float
    longitude: float