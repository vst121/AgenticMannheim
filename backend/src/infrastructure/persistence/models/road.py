from uuid import UUID

from sqlalchemy import Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RoadModel(Base):
    __tablename__ = "roads"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    road_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    start_intersection_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )
    end_intersection_id: Mapped[UUID] = mapped_column(
        nullable=False,
    )
    length_meters: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    speed_limit_kmh: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    lanes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    geometry: Mapped[list[dict[str, float]]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )