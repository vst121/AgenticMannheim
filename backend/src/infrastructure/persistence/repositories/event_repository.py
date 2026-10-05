from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.event import EventModel


class EventRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, event_id: UUID) -> EventModel | None:
        statement = select(EventModel).where(EventModel.id == event_id)
        return self._session.scalar(statement)

    def get_recent(self, limit: int = 100) -> list[EventModel]:
        statement = (
            select(EventModel)
            .order_by(EventModel.timestamp.desc())
            .limit(limit)
        )

        return list(self._session.scalars(statement).all())

    def add(self, event: EventModel) -> EventModel:
        self._session.add(event)
        self._session.flush()
        return event