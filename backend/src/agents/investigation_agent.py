
from math import cos, hypot, radians
from uuid import UUID

from digital_twin.twin import DigitalTwin
from domain.citizen_request import CitizenRequest
from domain.event import CityEvent
from domain.investigation import (
    Investigation,
    InvestigationFinding,
)
from infrastructure.persistence.repositories.citizen_request_repository import (
    CitizenRequestRepository,
)
from infrastructure.persistence.repositories.event_repository import (
    EventRepository,
)

METERS_PER_DEGREE_LATITUDE = 111_320

class InvestigationAgent:
    def __init__(
        self,
        digital_twin: DigitalTwin,
        request_repository: CitizenRequestRepository,
        event_repository: EventRepository,
        search_radius_meters: float = 300.0,
    ) -> None:
        if search_radius_meters <= 0:
            raise ValueError("Search radius must be greater than zero.")

        self._digital_twin = digital_twin
        self._request_repository = request_repository
        self._event_repository = event_repository
        self._search_radius_meters = search_radius_meters

    def investigate(self, request: CitizenRequest) -> Investigation:
        investigation = Investigation(
            request_id=request.id,
            correlation_id=request.correlation_id,
        )

        investigation.add_finding(
            InvestigationFinding(
                category="citizen_request",
                description=(
                    f"Request type: {request.request_type.value}. "
                    f"Description: {request.description}"
                ),
                source=f"citizen_request:{request.id}",
                confidence=1.0,
            )
        )

        related_requests = self._find_related_requests(request)
        for related_request in related_requests:
            investigation.related_request_ids.append(related_request.id)
            investigation.add_finding(
                InvestigationFinding(
                    category="related_citizen_request",
                    description=(
                        f"Nearby request of type "
                        f"{related_request.request_type.value}: "
                        f"{related_request.description}"
                    ),
                    source=f"citizen_request:{related_request.id}",
                    confidence=1.0,
                )
            )

        state = self._digital_twin.get_state()
        for intersection in state.intersections:
            distance = self._distance_meters(
                request.location.latitude,
                request.location.longitude,
                intersection.latitude,
                intersection.longitude,
            )

            if distance > self._search_radius_meters:
                continue

            investigation.add_finding(
                InvestigationFinding(
                    category="nearby_intersection",
                    description=(
                        f"Intersection '{intersection.name}' is "
                        f"approximately {distance:.0f} meters away. "
                        f"Traffic light present: "
                        f"{intersection.traffic_light is not None}."
                    ),
                    source=f"digital_twin:intersection:{intersection.id}",
                    confidence=1.0,
                )
            )

        for event in self._find_location_tagged_events(request):
            investigation.related_event_ids.append(event.id)
            investigation.add_finding(
                InvestigationFinding(
                    category="nearby_city_event",
                    description=(
                        f"Nearby event of type {event.event_type.value}."
                    ),
                    source=f"city_event:{event.id}",
                    confidence=1.0,
                )
            )

        return investigation

    def _find_related_requests(
        self,
        request: CitizenRequest,
    ) -> list[CitizenRequest]:
        candidates = self._request_repository.list_recent(limit=100)
        related: list[CitizenRequest] = []

        for candidate in candidates:
            if candidate.id == request.id:
                continue

            distance = self._distance_meters(
                request.location.latitude,
                request.location.longitude,
                candidate.location.latitude,
                candidate.location.longitude,
            )

            if distance <= self._search_radius_meters:
                related.append(candidate)

        return related

    def _find_location_tagged_events(
        self,
        request: CitizenRequest,
    ) -> list[CityEvent]:
        events = self._event_repository.get_recent(limit=100)
        related: list[CityEvent] = []

        for event in events:
            latitude = event.payload.get("latitude")
            longitude = event.payload.get("longitude")

            if not isinstance(latitude, (int, float)):
                continue
            if not isinstance(longitude, (int, float)):
                continue

            distance = self._distance_meters(
                request.location.latitude,
                request.location.longitude,
                float(latitude),
                float(longitude),
            )

            if distance <= self._search_radius_meters:
                related.append(event)

        return related

    @staticmethod
    def _distance_meters(
        latitude_a: float,
        longitude_a: float,
        latitude_b: float,
        longitude_b: float,
    ) -> float:
        mean_latitude = radians((latitude_a + latitude_b) / 2)
        latitude_delta = (latitude_b - latitude_a) * METERS_PER_DEGREE_LATITUDE
        longitude_delta = (
            (longitude_b - longitude_a)
            * METERS_PER_DEGREE_LATITUDE
            * cos(mean_latitude)
        )

        return hypot(latitude_delta, longitude_delta)
