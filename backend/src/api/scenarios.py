import random

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from domain.vehicle import VehicleType
from digital_twin.twin import DigitalTwin


MAP_MIN_LATITUDE = 49.4800
MAP_MAX_LATITUDE = 49.4950
MAP_MIN_LONGITUDE = 8.4530
MAP_MAX_LONGITUDE = 8.4800

MIN_DISTANCE_FROM_INTERSECTION_METERS = 50.0


class EmergencyScenarioResponse(BaseModel):
    vehicle_id: str
    road_id: str
    latitude: float
    longitude: float


router = APIRouter(
    prefix="/api/scenarios",
    tags=["Scenarios"],
)


@router.post(
    "/emergency",
    response_model=EmergencyScenarioResponse,
)
async def create_emergency_scenario(
    request: Request,
) -> EmergencyScenarioResponse:
    digital_twin: DigitalTwin = request.app.state.digital_twin
    twin_state = digital_twin.get_state()

    intersections_by_id = {
        intersection.id: intersection
        for intersection in twin_state.intersections
    }

    candidate_roads = [
        road
        for road in twin_state.roads
        if _is_valid_emergency_road(
            road,
            intersections_by_id,
        )
    ]

    print(
        "Emergency scenario candidate roads:",
        len(candidate_roads),
    )

    if not candidate_roads:
        raise HTTPException(
            status_code=404,
            detail=(
                "No suitable road is available for "
                "an emergency scenario."
            ),
        )

    # Randomly try valid roads until we find a valid
    # starting position inside the Digital Twin map.
    random.shuffle(candidate_roads)

    for road in candidate_roads:
        position = _random_start_position(road)

        if position is None:
            continue

        position_on_road_meters, latitude, longitude = position

        vehicle_id = digital_twin.add_vehicle(
            vehicle_type=VehicleType.EMERGENCY,
            latitude=latitude,
            longitude=longitude,
            speed_kmh=40.0,
            road_id=road.id,
            position_on_road_meters=position_on_road_meters,
        )

        return EmergencyScenarioResponse(
            vehicle_id=str(vehicle_id),
            road_id=str(road.id),
            latitude=latitude,
            longitude=longitude,
        )

    raise HTTPException(
        status_code=404,
        detail=(
            "Suitable emergency roads exist, "
            "but no valid starting position was found "
            "inside the map area."
        ),
    )


def _is_valid_emergency_road(
    road,
    intersections_by_id,
) -> bool:
    if len(road.geometry) < 2:
        return False

    destination = intersections_by_id.get(
        road.end_intersection_id,
    )

    if destination is None:
        return False

    # The emergency vehicle must eventually reach
    # an intersection controlled by a traffic light.
    if destination.traffic_light is None:
        return False

    # The road must be long enough to place the vehicle
    # at least 50 meters before the destination.
    if road.length_meters <= MIN_DISTANCE_FROM_INTERSECTION_METERS:
        return False

    return True


def _random_start_position(
    road,
) -> tuple[float, float, float] | None:
    # Keep the vehicle at least 50 meters from the
    # destination intersection.
    max_position = (
        road.length_meters
        - MIN_DISTANCE_FROM_INTERSECTION_METERS
    )

    if max_position <= 0:
        return None

    # Avoid spawning immediately at the beginning
    # of the road segment.
    min_position = min(
        road.length_meters * 0.1,
        max_position,
    )

    for _ in range(10):
        position = random.uniform(
            min_position,
            max_position,
        )

        latitude, longitude = _position_on_road(
            road=road,
            position_meters=position,
        )

        if _is_inside_map(latitude, longitude):
            return (
                position,
                latitude,
                longitude,
            )

    return None


def _is_inside_map(
    latitude: float,
    longitude: float,
) -> bool:
    return (
        MAP_MIN_LATITUDE <= latitude <= MAP_MAX_LATITUDE
        and MAP_MIN_LONGITUDE <= longitude <= MAP_MAX_LONGITUDE
    )


def _position_on_road(
    road,
    position_meters: float,
) -> tuple[float, float]:
    if position_meters <= 0:
        first = road.geometry[0]
        return first.latitude, first.longitude

    remaining = position_meters

    for first, second in zip(
        road.geometry,
        road.geometry[1:],
    ):
        segment_length = _distance_meters(
            first.latitude,
            first.longitude,
            second.latitude,
            second.longitude,
        )

        if remaining <= segment_length:
            if segment_length == 0:
                return first.latitude, first.longitude

            ratio = remaining / segment_length

            latitude = (
                first.latitude
                + (second.latitude - first.latitude) * ratio
            )

            longitude = (
                first.longitude
                + (second.longitude - first.longitude) * ratio
            )

            return latitude, longitude

        remaining -= segment_length

    last = road.geometry[-1]

    return last.latitude, last.longitude


def _distance_meters(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float,
) -> float:
    latitude_distance = (
        latitude2 - latitude1
    ) * 111_000

    longitude_distance = (
        longitude2 - longitude1
    ) * 111_000

    return (
        latitude_distance**2
        + longitude_distance**2
    ) ** 0.5
