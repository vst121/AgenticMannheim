from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class EventModel(Base):
    __tablename__ = "events"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    aggregate_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
    )

    correlation_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )

    payload: Mapped[dict[str, object]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )