from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from domain.vehicle import VehicleType
from digital_twin.twin import DigitalTwin


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

    roads = digital_twin.get_state().roads

    road = next(
        (
            road
            for road in roads
            if road.length_meters >= 200
            and len(road.geometry) >= 2
        ),
        None,
    )

    if road is None:
        raise HTTPException(
            status_code=404,
            detail="No suitable road is available.",
        )

    start = road.geometry[0]

    latitude = start.latitude
    longitude = start.longitude

    vehicle_id = digital_twin.add_vehicle(
        vehicle_type=VehicleType.EMERGENCY,
        latitude=latitude,
        longitude=longitude,
        speed_kmh=40.0,
        road_id=road.id,
        position_on_road_meters=0.0,
    )

    return EmergencyScenarioResponse(
        vehicle_id=str(vehicle_id),
        road_id=str(road.id),
        latitude=latitude,
        longitude=longitude,
    )