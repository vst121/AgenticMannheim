from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.event import CityEvent

from ..mappers.event_mapper import to_domain, to_model
from ..models.event import EventModel


class EventRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, event_id: UUID) -> CityEvent | None:
        statement = select(EventModel).where(EventModel.id == event_id)

        model = self._session.scalar(statement)

        if model is None:
            return None

        return to_domain(model)

    def get_recent(self, limit: int = 100) -> list[CityEvent]:
        statement = (
            select(EventModel)
            .order_by(EventModel.timestamp.desc())
            .limit(limit)
        )

        models = self._session.scalars(statement).all()

        return [to_domain(model) for model in models]

    def add(self, event: CityEvent) -> CityEvent:
        model = to_model(event)

        self._session.add(model)
        self._session.flush()

        return to_domain(model)