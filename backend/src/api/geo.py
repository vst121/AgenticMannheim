from typing import Literal

from pydantic import BaseModel


class GeoJSONPoint(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]


class GeoJSONLineString(BaseModel):
    type: Literal["LineString"] = "LineString"
    coordinates: list[tuple[float, float]]


class RoadFeatureProperties(BaseModel):
    id: str
    name: str
    road_type: str
    speed_limit_kmh: float
    lanes: int


class RoadFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: GeoJSONLineString
    properties: RoadFeatureProperties


class RoadFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[RoadFeature]