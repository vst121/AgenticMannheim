from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel

from digital_twin.twin import DigitalTwin


class IntersectionFeatureProperties(BaseModel):
    id: str
    name: str
    traffic_light: str | None


class IntersectionFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: dict
    properties: IntersectionFeatureProperties


class IntersectionFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[IntersectionFeature]


router = APIRouter(
    prefix="/api/intersections",
    tags=["Intersections"],
)


@router.get(
    "/geojson",
    response_model=IntersectionFeatureCollection,
)
async def get_intersections_geojson(
    request: Request,
) -> IntersectionFeatureCollection:
    digital_twin: DigitalTwin = request.app.state.digital_twin

    features: list[IntersectionFeature] = []

    for intersection in digital_twin.get_state().intersections:
        features.append(
            IntersectionFeature(
                geometry={
                    "type": "Point",
                    "coordinates": [
                        intersection.longitude,
                        intersection.latitude,
                    ],
                },
                properties=IntersectionFeatureProperties(
                    id=str(intersection.id),
                    name=intersection.name,
                    traffic_light=(
                        intersection.traffic_light.value
                        if intersection.traffic_light is not None
                        else None
                    ),
                ),
            )
        )

    return IntersectionFeatureCollection(
        features=features,
    )