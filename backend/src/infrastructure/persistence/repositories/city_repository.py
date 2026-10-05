from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.city import CityModel


class CityRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, city_id: UUID) -> CityModel | None:
        statement = select(CityModel).where(
            CityModel.id == city_id
        )

        return self._session.scalar(statement)

    def get_all(self) -> list[CityModel]:
        statement = select(CityModel)

        return list(self._session.scalars(statement).all())

    def add(self, city: CityModel) -> CityModel:
        self._session.add(city)
        self._session.flush()

        return city