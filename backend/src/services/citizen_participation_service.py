
from uuid import UUID

from domain.citizen_request import (
    CitizenRequest,
    CitizenRequestType,
)
from domain.event import CityEvent, CityEventType
from infrastructure.persistence.repositories.citizen_request_repository import (
    CitizenRequestRepository,
)
from infrastructure.persistence.repositories.event_repository import (
    EventRepository,
)


class CitizenParticipationService:
    def __init__(
        self,
        request_repository: CitizenRequestRepository,
        event_repository: EventRepository,
    ) -> None:
        self._request_repository = request_repository
        self._event_repository = event_repository

    def submit_request(
        self,
        request_type: CitizenRequestType,
        description: str,
        latitude: float,
        longitude: float,
    ) -> CitizenRequest:
        description = description.strip()

        if not description:
            raise ValueError("Request description must not be empty.")

        if not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")

        if not -180 <= longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180.")

        request = CitizenRequest(
            request_type=request_type,
            description=description,
            location=__import__(
                "domain.citizen_request",
                fromlist=["GeoLocation"],
            ).GeoLocation(
                latitude=latitude,
                longitude=longitude,
            ),
        )

        saved_request = self._request_repository.add(request)

        self._event_repository.add(
            CityEvent(
                event_type=CityEventType.CITIZEN_REQUEST_SUBMITTED,
                aggregate_id=saved_request.id,
                correlation_id=saved_request.correlation_id,
                payload={
                    "request_id": str(saved_request.id),
                    "request_type": saved_request.request_type.value,
                    "description": saved_request.description,
                    "latitude": latitude,
                    "longitude": longitude,
                },
            )
        )

        return saved_request
