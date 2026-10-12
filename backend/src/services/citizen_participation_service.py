
from uuid import UUID

from agents.investigation_agent import InvestigationAgent
from digital_twin.twin import DigitalTwin
from domain.citizen_request import (
    CitizenRequest,
    CitizenRequestType,
    GeoLocation,
)
from domain.event import CityEvent, CityEventType
from domain.investigation import Investigation
from infrastructure.persistence.repositories.citizen_request_repository import (
    CitizenRequestRepository,
)
from infrastructure.persistence.repositories.event_repository import (
    EventRepository,
)
from domain.intervention_proposal import (
    InterventionProposal,
    InterventionType,
)
from simulation.actions import SimulationAction
from policy.policy import CityPolicy, PolicyDecision

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
            location=GeoLocation(
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

    def investigate_request(
        self,
        request_id: UUID,
        digital_twin: DigitalTwin,
    ) -> Investigation:
        request = self._request_repository.get_by_id(request_id)

        if request is None:
            raise ValueError(
                f"Citizen request '{request_id}' was not found."
            )

        agent = InvestigationAgent(
            digital_twin=digital_twin,
            request_repository=self._request_repository,
            event_repository=self._event_repository,
        )

        return agent.investigate(request)

    def propose_intervention(
        self,
        request_id: UUID,
        digital_twin: DigitalTwin,
    ) -> InterventionProposal:
        investigation = self.investigate_request(
            request_id=request_id,
            digital_twin=digital_twin,
        )

        request = self._request_repository.get_by_id(request_id)
        if request is None:
            raise ValueError(f"Citizen request '{request_id}' was not found.")

        nearby_intersections = [
            finding
            for finding in investigation.findings
            if finding.category == "nearby_intersection"
        ]

        signalized_finding = next(
            (
                finding
                for finding in investigation.findings
                if finding.category == "nearest_signalized_intersection"
            ),
            None,
        )

        target_intersection_id: UUID | None = None

        if signalized_finding is not None:
            _, separator, intersection_id = signalized_finding.source.partition(
                "digital_twin:intersection:"
            )

            if separator:
                try:
                    target_intersection_id = UUID(intersection_id)
                except ValueError:
                    target_intersection_id = None

        if request.request_type.value == "safety_concern":
            intervention_type = InterventionType.PEDESTRIAN_SAFETY
            title = "Review pedestrian safety near the reported location"
            description = (
                "Assess pedestrian safety at the reported location. "
                f"The investigation identified "
                f"{len(nearby_intersections)} nearby intersections "
                "within the configured search radius."
            )
        elif request.request_type.value == "incident":
            intervention_type = InterventionType.FURTHER_INVESTIGATION
            title = "Investigate the reported traffic incident"
            description = (
                "Review the reported incident and the nearby Digital Twin "
                "context before deciding whether an intervention is needed."
            )
        else:
            intervention_type = InterventionType.FURTHER_INVESTIGATION
            title = "Review the citizen request"
            description = (
                "Review the request and gather additional evidence "
                "before recommending an intervention."
            )

        return InterventionProposal(
            request_id=request.id,
            investigation_id=investigation.id,
            intervention_type=intervention_type,
            title=title,
            description=description,
            target_intersection_id=target_intersection_id,
            expected_benefits=[
                "Provide a structured response to the citizen's concern."
            ],
            potential_risks=[
                "The available investigation data may not be sufficient "
                "to justify a real-world change."
            ],
            correlation_id=request.correlation_id,
        )

    def validate_intervention(
        self,
        proposal: InterventionProposal,
        digital_twin: DigitalTwin,
        traffic_light_state: str,
    ) -> PolicyDecision:
        action = self.to_simulation_action(
            proposal=proposal,
            traffic_light_state=traffic_light_state,
        )

        if action is None:
            return PolicyDecision(
                allowed=False,
                reason=(
                    "The proposal cannot be converted into a traffic-light "
                    "simulation action."
                ),
            )

        policy = CityPolicy(digital_twin)
        return policy.validate(action)

    @staticmethod
    def to_simulation_action(
        proposal: InterventionProposal,
        traffic_light_state: str,
    ) -> SimulationAction | None:
        if proposal.intervention_type != InterventionType.TRAFFIC_LIGHT_ADJUSTMENT:
            return None

        if proposal.target_intersection_id is None:
            return None

        return SimulationAction(
            intersection_id=proposal.target_intersection_id,
            traffic_light_state=traffic_light_state,
        )