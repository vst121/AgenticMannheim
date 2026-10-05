from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class CityModel(Base):
    __tablename__ = "cities"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    area: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    latitude: Mapped[float] = mapped_column(
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        nullable=False,
    )