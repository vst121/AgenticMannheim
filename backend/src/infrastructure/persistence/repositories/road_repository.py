from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.road import Road

from ..mappers.road_mapper import to_domain, to_model
from ..models.road import RoadModel


class RoadRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, road_id: UUID) -> Road | None:
        statement = select(RoadModel).where(RoadModel.id == road_id)
        model = self._session.scalar(statement)

        if model is None:
            return None

        return to_domain(model)

    def get_all(self) -> list[Road]:
        statement = select(RoadModel)
        models = self._session.scalars(statement).all()

        return [to_domain(model) for model in models]

    def add(self, road: Road) -> Road:
        model = to_model(road)

        self._session.add(model)
        self._session.flush()

        return to_domain(model)