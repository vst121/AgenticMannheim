from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Float, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from domain.citizen_request import (
    CitizenRequest,
    CitizenRequestStatus,
    CitizenRequestType,
)
from infrastructure.persistence.models.base import Base


class CitizenRequestModel(Base):
    __tablename__ = "citizen_requests"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
    )

    request_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
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

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default=CitizenRequestStatus.SUBMITTED.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    correlation_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_citizen_requests_correlation_id",
            "correlation_id",
        ),
        Index(
            "ix_citizen_requests_status",
            "status",
        ),
        Index(
            "ix_citizen_requests_created_at",
            "created_at",
        ),
    )

    @classmethod
    def from_domain(cls, request: "CitizenRequest") -> "CitizenRequestModel":
        return cls(
            id=request.id,
            request_type=request.request_type.value,
            description=request.description,
            latitude=request.location.latitude,
            longitude=request.location.longitude,
            status=request.status.value,
            created_at=request.created_at,
            correlation_id=request.correlation_id,
        )

    def to_domain(self) -> "CitizenRequest":
        from domain.citizen_request import CitizenRequest, GeoLocation

        return CitizenRequest(
            id=self.id,
            request_type=CitizenRequestType(self.request_type),
            description=self.description,
            location=GeoLocation(
                latitude=self.latitude,
                longitude=self.longitude,
            ),
            status=CitizenRequestStatus(self.status),
            created_at=self.created_at,
            correlation_id=self.correlation_id,
        )