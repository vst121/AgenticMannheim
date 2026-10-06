import digital_twin
from fastapi import APIRouter, Request

from api.geo import (
    GeoJSONLineString,
    RoadFeature,
    RoadFeatureCollection,
    RoadFeatureProperties,
)
from digital_twin.twin import DigitalTwin

router = APIRouter(
    prefix="/api/roads",
    tags=["Roads"],
)


@router.get(
    "/geojson",
    response_model=RoadFeatureCollection,
)
async def get_roads_geojson(
    request: Request,
) -> RoadFeatureCollection:
    digital_twin: DigitalTwin = request.app.state.digital_twin

    roads = digital_twin.get_state().roads

    print(f"Digital Twin roads: {len(roads)}")

    if roads:
        print(f"First road: {roads[0].name}")
        print(f"First road geometry points: {len(roads[0].geometry)}")

    features: list[RoadFeature] = []

    for road in digital_twin.get_state().roads:
        if len(road.geometry) < 2:
            continue

        coordinates = [
            (
                point.longitude,
                point.latitude,
            )
            for point in road.geometry
        ]

        features.append(
            RoadFeature(
                geometry=GeoJSONLineString(
                    coordinates=coordinates,
                ),
                properties=RoadFeatureProperties(
                    id=str(road.id),
                    name=road.name,
                    road_type=road.road_type.value,
                    speed_limit_kmh=road.speed_limit_kmh,
                    lanes=road.lanes,
                ),
            )
        )

    return RoadFeatureCollection(
        features=features,
    )