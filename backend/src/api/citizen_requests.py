
from datetime import datetime
from uuid import UUID
import digital_twin
from domain.intervention_evaluation import InterventionEvaluation
from fastapi import APIRouter, Depends, HTTPException, Request, status
from httpcore import request
from infrastructure.persistence.repositories.intervention_evaluation_repository import InterventionEvaluationRepository
from infrastructure.persistence.repositories.intervention_proposal_repository import InterventionProposalRepository
from pydantic import BaseModel, ConfigDict, Field
from services.intervention_evaluation_service import InterventionEvaluationService
from sqlalchemy.orm import Session

from domain.citizen_request import (
    CitizenRequest,
    CitizenRequestType,
)
from infrastructure.persistence.database import get_session
from infrastructure.persistence.repositories.citizen_request_repository import (
    CitizenRequestRepository,
)
from infrastructure.persistence.repositories.event_repository import (
    EventRepository,
)
from services.citizen_participation_service import (
    CitizenParticipationService,
)
from digital_twin.twin import DigitalTwin
from domain.investigation import Investigation
from domain.intervention_proposal import InterventionProposal


router = APIRouter(
    prefix="/api/citizen-requests",
    tags=["Citizen Participation"],
)


class CitizenRequestCreate(BaseModel):
    request_type: CitizenRequestType
    description: str = Field(min_length=1, max_length=5000)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class CitizenRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    request_type: CitizenRequestType
    description: str
    latitude: float
    longitude: float
    status: str
    created_at: datetime
    correlation_id: UUID

    @classmethod
    def from_domain(
        cls,
        request: CitizenRequest,
    ) -> "CitizenRequestResponse":
        return cls(
            id=request.id,
            request_type=request.request_type,
            description=request.description,
            latitude=request.location.latitude,
            longitude=request.location.longitude,
            status=request.status.value,
            created_at=request.created_at,
            correlation_id=request.correlation_id,
        )


class InvestigationFindingResponse(BaseModel):
    category: str
    description: str
    source: str
    confidence: float


class InvestigationResponse(BaseModel):
    id: UUID
    request_id: UUID
    status: str
    findings: list[InvestigationFindingResponse]
    related_request_ids: list[UUID]
    related_event_ids: list[UUID]
    correlation_id: UUID

    @classmethod
    def from_domain(
        cls,
        investigation: Investigation,
    ) -> "InvestigationResponse":
        return cls(
            id=investigation.id,
            request_id=investigation.request_id,
            status=investigation.status.value,
            findings=[
                InvestigationFindingResponse(
                    category=finding.category,
                    description=finding.description,
                    source=finding.source,
                    confidence=finding.confidence,
                )
                for finding in investigation.findings
            ],
            related_request_ids=investigation.related_request_ids,
            related_event_ids=investigation.related_event_ids,
            correlation_id=investigation.correlation_id,
        )

class InterventionProposalResponse(BaseModel):
    id: UUID
    request_id: UUID
    investigation_id: UUID
    intervention_type: str
    title: str
    description: str
    target_intersection_id: UUID | None
    expected_benefits: list[str]
    potential_risks: list[str]
    status: str
    correlation_id: UUID

    @classmethod
    def from_domain(
        cls,
        proposal: InterventionProposal,
    ) -> "InterventionProposalResponse":
        return cls(
            id=proposal.id,
            request_id=proposal.request_id,
            investigation_id=proposal.investigation_id,
            intervention_type=proposal.intervention_type.value,
            title=proposal.title,
            description=proposal.description,
            target_intersection_id=proposal.target_intersection_id,
            expected_benefits=proposal.expected_benefits,
            potential_risks=proposal.potential_risks,
            status=proposal.status.value,
            correlation_id=proposal.correlation_id,
        )

class PolicyDecisionResponse(BaseModel):
    allowed: bool
    reason: str

class EvaluationFindingResponse(BaseModel):
    category: str
    description: str
    source: str
    confidence: float

class InterventionEvaluationResponse(BaseModel):
    id: UUID
    proposal_id: UUID
    outcome: str
    summary: str
    findings: list[EvaluationFindingResponse]
    expected_benefits: list[str]
    potential_risks: list[str]
    created_at: datetime
    correlation_id: UUID

    @classmethod
    def from_domain(
        cls, evaluation: InterventionEvaluation
    ) -> "InterventionEvaluationResponse":
        return cls(
            id=evaluation.id,
            proposal_id=evaluation.proposal_id,
            outcome=evaluation.outcome.value,
            summary=evaluation.summary,
            findings=[
                EvaluationFindingResponse(
                    category=finding.category,
                    description=finding.description,
                    source=finding.source,
                    confidence=finding.confidence,
                )
                for finding in evaluation.findings
            ],
            expected_benefits=evaluation.expected_benefits,
            potential_risks=evaluation.potential_risks,
            created_at=evaluation.created_at,
            correlation_id=evaluation.correlation_id,
        )

@router.post(
    "",
    response_model=CitizenRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_citizen_request(
    payload: CitizenRequestCreate,
    session: Session = Depends(get_session),
) -> CitizenRequestResponse:
    try:
        with session.begin():
            service = CitizenParticipationService(
                request_repository=CitizenRequestRepository(session),
                event_repository=EventRepository(session),
                intervention_proposal_repository=InterventionProposalRepository(session),                    
            )
            request = service.submit_request(
                request_type=payload.request_type,
                description=payload.description,
                latitude=payload.latitude,
                longitude=payload.longitude,
            )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return CitizenRequestResponse.from_domain(request)


@router.get(
    "/{request_id}/investigation",
    response_model=InvestigationResponse,
)
def investigate_citizen_request(
    request_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
) -> InvestigationResponse:
    service = CitizenParticipationService(
        request_repository=CitizenRequestRepository(session),
        event_repository=EventRepository(session),
        intervention_proposal_repository=InterventionProposalRepository(session),
    )

    digital_twin: DigitalTwin = request.app.state.digital_twin

    try:
        investigation = service.investigate_request(
            request_id=request_id,
            digital_twin=digital_twin,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return InvestigationResponse.from_domain(investigation)


@router.post(
    "/{request_id}/proposal",
    response_model=InterventionProposalResponse,
)
def propose_citizen_intervention(
    request_id: UUID,
    request: Request,
    session: Session = Depends(get_session),
) -> InterventionProposalResponse:
    digital_twin: DigitalTwin = request.app.state.digital_twin

    try:
        with session.begin():
            service = CitizenParticipationService(
                request_repository=CitizenRequestRepository(session),
                event_repository=EventRepository(session),
                intervention_proposal_repository=(
                    InterventionProposalRepository(session)
                ),
            )

            proposal = service.propose_intervention(
                request_id=request_id,
                digital_twin=digital_twin,
            )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return InterventionProposalResponse.from_domain(proposal)

@router.get(
    "/{request_id}/proposals",
    response_model=list[InterventionProposalResponse],
)
def list_request_proposals(
    request_id: UUID,
    session=Depends(get_session),
):
    request_repository = CitizenRequestRepository(session)
    proposal_repository = InterventionProposalRepository(session)

    citizen_request = request_repository.get_by_id(request_id)
    if citizen_request is None:
        raise HTTPException(
            status_code=404,
            detail=f"Citizen request '{request_id}' was not found.",
        )

    proposals = proposal_repository.list_by_request(request_id)

    return [
        InterventionProposalResponse.from_domain(proposal)
        for proposal in proposals
    ]

@router.post(
    "/proposals/{proposal_id}/evaluations",
    response_model=InterventionEvaluationResponse,
    status_code=201,
)
def evaluate_intervention_proposal(
    proposal_id: UUID,
    request: Request,
    session=Depends(get_session),
):
    try:
        with session.begin():
            service = InterventionEvaluationService(
                proposal_repository=InterventionProposalRepository(session),
                request_repository=CitizenRequestRepository(session),
                event_repository=EventRepository(session),
                evaluation_repository=InterventionEvaluationRepository(session),
                digital_twin=request.app.state.digital_twin,
            )
            evaluation = service.evaluate(proposal_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return InterventionEvaluationResponse.from_domain(evaluation)