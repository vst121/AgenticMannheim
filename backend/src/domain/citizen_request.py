from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


@dataclass(frozen=True)
class GeoLocation:
    latitude: float
    longitude: float


class CitizenRequestType(StrEnum):
    INCIDENT = "incident"
    SAFETY_CONCERN = "safety_concern"
    SUGGESTION = "suggestion"
    GENERAL_REQUEST = "general_request"


class CitizenRequestStatus(StrEnum):
    SUBMITTED = "submitted"
    INVESTIGATING = "investigating"
    PROPOSED = "proposed"
    EVALUATED = "evaluated"
    COMPLETED = "completed"


@dataclass
class CitizenRequest:
    id: UUID = field(default_factory=uuid4)
    request_type: CitizenRequestType = CitizenRequestType.GENERAL_REQUEST
    description: str = ""
    location: GeoLocation = field(
        default_factory=lambda: GeoLocation(
            latitude=0.0,
            longitude=0.0,
        )
    )
    status: CitizenRequestStatus = CitizenRequestStatus.SUBMITTED
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    correlation_id: UUID = field(default_factory=uuid4)

    def start_investigation(self) -> None:
        self.status = CitizenRequestStatus.INVESTIGATING

    def mark_proposed(self) -> None:
        self.status = CitizenRequestStatus.PROPOSED

    def mark_evaluated(self) -> None:
        self.status = CitizenRequestStatus.EVALUATED

    def complete(self) -> None:
        self.status = CitizenRequestStatus.COMPLETED    