from uuid import UUID

from agents.investigation_agent import InvestigationAgent
from digital_twin.twin import DigitalTwin
from domain.intervention_evaluation import (
    EvaluationFinding,
    EvaluationOutcome,
    InterventionEvaluation,
)
from infrastructure.persistence.repositories.citizen_request_repository import (
    CitizenRequestRepository,
)
from infrastructure.persistence.repositories.event_repository import (
    EventRepository,
)
from infrastructure.persistence.repositories.intervention_proposal_repository import (
    InterventionProposalRepository,
)
from infrastructure.persistence.repositories.intervention_evaluation_repository import (
    InterventionEvaluationRepository,
)

class InterventionEvaluationService:
    def __init__(
        self,
        proposal_repository: InterventionProposalRepository,
        request_repository: CitizenRequestRepository,
        event_repository: EventRepository,
        evaluation_repository: InterventionEvaluationRepository,
        digital_twin: DigitalTwin,
    ) -> None:
        self._proposal_repository = proposal_repository
        self._request_repository = request_repository
        self._event_repository = event_repository
        self._evaluation_repository = evaluation_repository
        self._digital_twin = digital_twin

    def evaluate(self, proposal_id: UUID) -> InterventionEvaluation:
        proposal = self._proposal_repository.get_by_id(proposal_id)
        if proposal is None:
            raise ValueError(
                f"Intervention proposal '{proposal_id}' was not found."
            )

        request = self._request_repository.get_by_id(proposal.request_id)
        if request is None:
            raise ValueError(
                f"Citizen request '{proposal.request_id}' was not found."
            )

        investigation_agent = InvestigationAgent(
            digital_twin=self._digital_twin,
            request_repository=self._request_repository,
            event_repository=self._event_repository,
        )
        investigation = investigation_agent.investigate(request)

        evaluation = InterventionEvaluation(
            proposal_id=proposal.id,
            outcome=EvaluationOutcome.INCONCLUSIVE,
            summary=(
                "Current investigation evidence has been collected. "
                "A reliable outcome requires defined evaluation criteria "
                "for assessing the proposed intervention."
            ),
            expected_benefits=list(proposal.expected_benefits),
            potential_risks=list(proposal.potential_risks),
            correlation_id=proposal.correlation_id,
        )

        for finding in investigation.findings:
            evaluation.add_finding(
                EvaluationFinding(
                    category=finding.category,
                    description=finding.description,
                    source=finding.source,
                    confidence=finding.confidence,
                )
            )

        if not investigation.findings:
            evaluation.add_finding(
                EvaluationFinding(
                    category="evidence_gap",
                    description=(
                        "The investigation did not produce findings. "
                        "Additional evidence may be needed to assess "
                        "the proposal."
                    ),
                    source="citizen_participation:investigation",
                    confidence=1.0,
                )
            )

        return self._evaluation_repository.add(evaluation)
