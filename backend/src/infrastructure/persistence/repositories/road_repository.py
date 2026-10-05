from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.road import RoadModel


class RoadRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, road_id: UUID) -> RoadModel | None:
        statement = select(RoadModel).where(RoadModel.id == road_id)
        return self._session.scalar(statement)

    def get_all(self) -> list[RoadModel]:
        statement = select(RoadModel)
        return list(self._session.scalars(statement).all())

    def add(self, road: RoadModel) -> RoadModel:
        self._session.add(road)
        self._session.flush()
        return road