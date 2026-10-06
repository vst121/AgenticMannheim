from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.city import CityMetadata

from ..mappers.city_mapper import to_domain, to_model
from ..models.city import CityModel


class CityRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, city_id: UUID) -> CityMetadata | None:
        statement = select(CityModel).where(CityModel.id == city_id)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return to_domain(model)

    def get_all(self) -> list[CityMetadata]:
        statement = select(CityModel)
        models = self._session.scalars(statement).all()

        return [to_domain(model) for model in models]

    def get_by_name(self, name: str) -> CityMetadata | None:
        statement = select(CityModel).where(
            CityModel.name == name,
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return to_domain(model)    

    def add(self, city: CityMetadata) -> CityMetadata:
        model = to_model(city)

        self._session.add(model)
        self._session.flush()

        return to_domain(model)