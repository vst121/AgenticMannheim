import asyncio

from infrastructure.geodata.osm import OSMRoadLoader
from infrastructure.geodata.osm_mapper import OSMMapper
from infrastructure.persistence.database import SessionLocal, settings
from infrastructure.persistence.repositories.intersection_repository import (
    IntersectionRepository,
)
from infrastructure.persistence.repositories.road_repository import (
    RoadRepository,
)


async def main() -> None:
    print("Loading Mannheim Innenstadt road network from OpenStreetMap...")

    loader = OSMRoadLoader(
        overpass_url=settings.overpass_url,
    )

    osm_roads = await loader.load_roads()

    print(f"Downloaded {len(osm_roads)} OSM roads.")

    mapper = OSMMapper()

    roads, intersections = mapper.map_roads(
        osm_roads,
    )

    print(f"Mapped {len(intersections)} intersections.")
    print(f"Mapped {len(roads)} road segments.")

    with SessionLocal() as session:
        intersection_repository = IntersectionRepository(
            session,
        )

        road_repository = RoadRepository(
            session,
        )

        for intersection in intersections:
            intersection_repository.add(
                intersection,
            )

        for road in roads:
            road_repository.add(
                road,
            )

        session.commit()

    print("OSM road network imported successfully.")


if __name__ == "__main__":
    asyncio.run(main())