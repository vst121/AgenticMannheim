import asyncio
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

    async def load_roads(self) -> list[OSMRoad]:
        # Filter for drivable road types to dramatically speed up Overpass execution
        query = """
        [out:json][timeout:180];
        (
          way["highway"~"motorway|trunk|primary|secondary|tertiary|unclassified|residential|living_street"](49.4800,8.4550,49.4920,8.4780);
        );
        out body geom;
        """

        endpoints = [
            self._overpass_url,
            "https://overpass-api.de/api/interpreter",
            "https://overpass.kumi.systems/api/interpreter",
            "https://overpass.openstreetmap.fr/api/interpreter",
        ]

        # Deduplicate endpoints while keeping order
        unique_endpoints = list(dict.fromkeys(endpoints))

        data = None
        async with httpx.AsyncClient(
            timeout=180.0,
            headers={
                "User-Agent": "AgenticMannheim/0.1",
                "Accept": "application/json",
            },
        ) as client:
            for url in unique_endpoints:
                for attempt in range(2):  # Retry up to 2 times per endpoint
                    try:
                        response = await client.post(
                            url,
                            content=query,
                            headers={
                                "Content-Type": "text/plain; charset=utf-8",
                            },
                        )
                        response.raise_for_status()
                        data = response.json()
                        break
                    except (httpx.HTTPError, httpx.TimeoutException):
                        if attempt < 1:
                            await asyncio.sleep(2)
                        continue
                if data is not None:
                    break

        if data is None:
            raise RuntimeError(
                "Failed to fetch OSM data from all Overpass API endpoints due to timeout or server errors."
            )

        roads: list[OSMRoad] = []

        for element in data.get("elements", []):
            geometry = element.get("geometry", [])
            node_ids = element.get("nodes", [])

            if len(geometry) < 2 or len(node_ids) != len(geometry):
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
                            id=node_id,
                            latitude=point["lat"],
                            longitude=point["lon"],
                        )
                        for node_id, point in zip(node_ids, geometry)
                    ),
                )
            )

        return roads

    @staticmethod
    def _parse_speed(value: str | None) -> float:
        if not value:
            return 50.0

        try:
            return float(value.split()[0])
        except ValueError:
            return 50.0

    @staticmethod
    def _parse_lanes(value: str | None) -> int:
        if not value:
            return 1

        try:
            return max(1, int(value))
        except ValueError:
            return 1