from domain.city import CityMetadata

from ..models.city import CityModel


def to_domain(model: CityModel) -> CityMetadata:
    return CityMetadata(
        name=model.name,
        area=model.area,
        latitude=model.latitude,
        longitude=model.longitude,
    )


def to_model(city: CityMetadata) -> CityModel:
    return CityModel(
        name=city.name,
        area=city.area,
        latitude=city.latitude,
        longitude=city.longitude,
    )