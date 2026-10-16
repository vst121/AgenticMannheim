from uuid import UUID

from agents.intervention_evaluation_agent import InterventionEvaluationAgent
from agents.investigation_agent import InvestigationAgent
from digital_twin.twin import DigitalTwin
from domain.intervention_evaluation import (
    EvaluationFinding,
    InterventionEvaluation,
)
from infrastructure.ai.fake_llm_client import FakeLLMClient
from infrastructure.ai.jev_client import JevClient
from infrastructure.ai.openrouter_client import OpenRouterClient
from infrastructure.persistence.repositories.citizen_request_repository import (
    CitizenRequestRepository,
)
from infrastructure.persistence.repositories.event_repository import (
    EventRepository,
)
from infrastructure.persistence.repositories.intervention_evaluation_repository import (
    InterventionEvaluationRepository,
)
from infrastructure.persistence.repositories.intervention_proposal_repository import (
    InterventionProposalRepository,
)


class InterventionEvaluationService:
    def __init__(
        self,
        proposal_repository: InterventionProposalRepository,
        request_repository: CitizenRequestRepository,
        event_repository: EventRepository,
        evaluation_repository: InterventionEvaluationRepository,
        digital_twin: DigitalTwin,
        evaluation_agent: InterventionEvaluationAgent | None = None,
        jev_client: JevClient | None = None,
    ) -> None:
        self._proposal_repository = proposal_repository
        self._request_repository = request_repository
        self._event_repository = event_repository
        self._evaluation_repository = evaluation_repository
        self._digital_twin = digital_twin
        self._evaluation_agent = evaluation_agent or (
            InterventionEvaluationAgent(FakeLLMClient()) # InterventionEvaluationAgent(OpenRouterClient())
        )
        self._jev_client = jev_client or JevClient()

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

        try:
            evaluation = self._evaluation_agent.evaluate(
                request=request,
                proposal=proposal,
                investigation=investigation,
            )
        except Exception as exc:
            raise RuntimeError(
                f"OpenRouter intervention evaluation failed "
                f"for proposal '{proposal_id}': "
                f"{type(exc).__name__}: {exc}"
            ) from exc

        try:
            jev_assessment, jev_confidence = self._jev_client.assess_evidence(
                request_description=request.description,
                proposal_description=(
                    f"{proposal.title}\n{proposal.description}"
                ),
                findings=[
                    {
                        "category": finding.category,
                        "description": finding.description,
                        "source": finding.source,
                        "confidence": finding.confidence,
                    }
                    for finding in investigation.findings
                ],
            )
        except Exception as exc:
            raise RuntimeError(
                f"Jev evidence assessment failed "
                f"for proposal '{proposal_id}': "
                f"{type(exc).__name__}: {exc}"
            ) from exc

        evaluation.add_finding(
            EvaluationFinding(
                category="jev_evidence_assessment",
                description=(
                    f"Jev assessed the evidence as '{jev_assessment}'."
                ),
                source="typesafe:jev",
                confidence=jev_confidence,
            )
        )

        saved_evaluation = self._evaluation_repository.add(evaluation)

        proposal.mark_evaluated()
        self._proposal_repository.update(proposal)

        return saved_evaluation