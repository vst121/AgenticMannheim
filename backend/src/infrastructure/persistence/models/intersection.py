from uuid import UUID

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class IntersectionModel(Base):
    __tablename__ = "intersections"

    id: Mapped[UUID] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    traffic_light: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )