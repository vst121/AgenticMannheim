import random

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from domain.vehicle import VehicleType
from digital_twin.twin import DigitalTwin


MAP_MIN_LATITUDE = 49.4800
MAP_MAX_LATITUDE = 49.4950
MAP_MIN_LONGITUDE = 8.4530
MAP_MAX_LONGITUDE = 8.4800


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

    roads = [
        road
        for road in digital_twin.get_state().roads
        if road.length_meters >= 200
        and len(road.geometry) >= 2
        and _road_is_inside_map(road)
    ]

    if not roads:
        raise HTTPException(
            status_code=404,
            detail="No suitable road is available inside the map area.",
        )

    road = random.choice(roads)

    max_start_position = road.length_meters * 0.8

    position_on_road_meters = random.uniform(
        0.0,
        max_start_position,
    )

    latitude, longitude = _position_on_road(
        road=road,
        position_meters=position_on_road_meters,
    )

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


def _road_is_inside_map(road) -> bool:
    return all(
        MAP_MIN_LATITUDE <= point.latitude <= MAP_MAX_LATITUDE
        and MAP_MIN_LONGITUDE <= point.longitude <= MAP_MAX_LONGITUDE
        for point in road.geometry
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
