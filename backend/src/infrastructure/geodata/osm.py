from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class OSMNode:
    id: int
    latitude: float
    longitude: float


@dataclass(frozen=True)
class OSMRoad:
    osm_id: int
    name: str
    road_type: str
    speed_limit_kmh: float
    lanes: int
    nodes: tuple[OSMNode, ...]


class OSMRoadLoader:
    def __init__(self, overpass_url: str) -> None:
        self._overpass_url = overpass_url

    async def load_roads(
        self,
        south: float,
        west: float,
        north: float,
        east: float,
    ) -> list[OSMRoad]:
        query = f"""
        [out:json][timeout:60];

        way["highway"]
            ({south},{west},{north},{east});

        out body geom;
        """

        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                self._overpass_url,
                data=query,
            )

        response.raise_for_status()

        data = response.json()

        roads: list[OSMRoad] = []

        for element in data.get("elements", []):
            geometry = element.get("geometry", [])

            if len(geometry) < 2:
                continue

            tags = element.get("tags", {})

            roads.append(
                OSMRoad(
                    osm_id=element["id"],
                    name=tags.get("name", "Unnamed road"),
                    road_type=tags.get(
                        "highway",
                        "service",
                    ),
                    speed_limit_kmh=self._parse_speed(
                        tags.get("maxspeed")
                    ),
                    lanes=self._parse_lanes(
                        tags.get("lanes")
                    ),
                    nodes=tuple(
                        OSMNode(
                            id=point["id"],
                            latitude=point["lat"],
                            longitude=point["lon"],
                        )
                        for point in geometry
                    ),
                )
            )

        return roads

    @staticmethod
    def _parse_speed(
        value: str | None,
    ) -> float:
        if not value:
            return 50.0

        try:
            return float(value.split()[0])
        except ValueError:
            return 50.0

    @staticmethod
    def _parse_lanes(
        value: str | None,
    ) -> int:
        if not value:
            return 1

        try:
            return max(1, int(value))
        except ValueError:
            return 1