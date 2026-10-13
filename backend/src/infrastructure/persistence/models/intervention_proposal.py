from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, JSON, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from domain.intervention_proposal import (
    InterventionProposal,
    InterventionStatus,
    InterventionType,
)
from infrastructure.persistence.models.base import Base


class InterventionProposalModel(Base):
    __tablename__ = "intervention_proposals"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
    )
    request_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("citizen_requests.id"),
        nullable=False,
        index=True,
    )
    investigation_id: Mapped[UUID] = mapped_column(
        Uuid,
        nullable=False,
    )
    intervention_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    target_intersection_id: Mapped[UUID | None] = mapped_column(
        Uuid,
        nullable=True,
    )
    expected_benefits: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    potential_risks: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    correlation_id: Mapped[UUID] = mapped_column(
        Uuid,
        nullable=False,
        index=True,
    )

    @classmethod
    def from_domain(
        cls,
        proposal: InterventionProposal,
    ) -> "InterventionProposalModel":
        return cls(
            id=proposal.id,
            request_id=proposal.request_id,
            investigation_id=proposal.investigation_id,
            intervention_type=proposal.intervention_type.value,
            title=proposal.title,
            description=proposal.description,
            target_intersection_id=proposal.target_intersection_id,
            expected_benefits=list(proposal.expected_benefits),
            potential_risks=list(proposal.potential_risks),
            status=proposal.status.value,
            created_at=proposal.created_at,
            correlation_id=proposal.correlation_id,
        )

    def to_domain(self) -> InterventionProposal:
        return InterventionProposal(
            id=self.id,
            request_id=self.request_id,
            investigation_id=self.investigation_id,
            intervention_type=InterventionType(self.intervention_type),
            title=self.title,
            description=self.description,
            target_intersection_id=self.target_intersection_id,
            expected_benefits=list(self.expected_benefits),
            potential_risks=list(self.potential_risks),
            status=InterventionStatus(self.status),
            created_at=self.created_at,
            correlation_id=self.correlation_id,
        )

