
from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, Field
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
