from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.intersection import Intersection

from ..mappers.intersection_mapper import to_domain, to_model
from ..models.intersection import IntersectionModel


class IntersectionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, intersection_id: UUID) -> Intersection | None:
        statement = select(IntersectionModel).where(
            IntersectionModel.id == intersection_id
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return to_domain(model)

    def get_all(self) -> list[Intersection]:
        statement = select(IntersectionModel)
        models = self._session.scalars(statement).all()

        return [to_domain(model) for model in models]

    def add(self, intersection: Intersection) -> Intersection:
        model = to_model(intersection)

        self._session.add(model)
        self._session.flush()

        return to_domain(model)
