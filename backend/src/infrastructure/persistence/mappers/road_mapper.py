from domain.road import Road, RoadType

from ..models.road import RoadModel


def to_domain(model: RoadModel) -> Road:
    return Road(
        id=model.id,
        name=model.name,
        road_type=RoadType(model.road_type),
        start_intersection_id=model.start_intersection_id,
        end_intersection_id=model.end_intersection_id,
        length_meters=model.length_meters,
        speed_limit_kmh=model.speed_limit_kmh,
        lanes=model.lanes,
    )


def to_model(road: Road) -> RoadModel:
    return RoadModel(
        id=road.id,
        name=road.name,
        road_type=road.road_type.value,
        start_intersection_id=road.start_intersection_id,
        end_intersection_id=road.end_intersection_id,
        length_meters=road.length_meters,
        speed_limit_kmh=road.speed_limit_kmh,
        lanes=road.lanes,
    )