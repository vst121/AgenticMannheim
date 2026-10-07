from domain.intersection import Intersection, TrafficLightState

from ..models.intersection import IntersectionModel


def to_domain(model: IntersectionModel) -> Intersection:
    return Intersection(
        intersection_id=model.id,
        name=model.name,
        latitude=model.latitude,
        longitude=model.longitude,
        traffic_light=(
            TrafficLightState(model.traffic_light)
            if model.traffic_light is not None
            else None
        ),
    )


def to_model(intersection: Intersection) -> IntersectionModel:
    return IntersectionModel(
        id=intersection.id,
        name=intersection.name,
        latitude=intersection.latitude,
        longitude=intersection.longitude,
        traffic_light=(
            intersection.traffic_light.value
            if intersection.traffic_light is not None
            else None
        ),
    )