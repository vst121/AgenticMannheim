from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel

from digital_twin.twin import DigitalTwin


class VehicleFeatureProperties(BaseModel):
    id: str
    vehicle_type: str
    speed_kmh: float
    road_id: str | None
    position_on_road_meters: float


class VehicleFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: dict
    properties: VehicleFeatureProperties


class VehicleFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[VehicleFeature]


router = APIRouter(
    prefix="/api/vehicles",
    tags=["Vehicles"],
)


@router.get(
    "/geojson",
    response_model=VehicleFeatureCollection,
)
async def get_vehicles_geojson(
    request: Request,
) -> VehicleFeatureCollection:
    digital_twin: DigitalTwin = request.app.state.digital_twin

    features: list[VehicleFeature] = []

    for vehicle in digital_twin.get_state().vehicles:
        features.append(
            VehicleFeature(
                geometry={
                    "type": "Point",
                    "coordinates": [
                        vehicle.longitude,
                        vehicle.latitude,
                    ],
                },
                properties=VehicleFeatureProperties(
                    id=str(vehicle.id),
                    vehicle_type=vehicle.type.value,
                    speed_kmh=vehicle.speed_kmh,
                    road_id=(
                        str(vehicle.road_id)
                        if vehicle.road_id
                        else None
                    ),
                    position_on_road_meters=(
                        vehicle.position_on_road_meters
                    ),
                ),
            )
        )

    return VehicleFeatureCollection(
        features=features,
    )