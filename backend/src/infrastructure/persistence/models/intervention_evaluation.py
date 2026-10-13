from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, JSON, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from domain.intervention_evaluation import (
    EvaluationFinding,
    EvaluationOutcome,
    InterventionEvaluation,
)
from infrastructure.persistence.models.base import Base


class InterventionEvaluationModel(Base):
    __tablename__ = "intervention_evaluations"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    proposal_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("intervention_proposals.id"),
        nullable=False,
        index=True,
    )
    outcome: Mapped[str] = mapped_column(String(30), nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    findings: Mapped[list[dict[str, object]]] = mapped_column(
        JSON, nullable=False, default=list
    )
    expected_benefits: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    potential_risks: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=list
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    correlation_id: Mapped[UUID] = mapped_column(
        Uuid, nullable=False, index=True
    )

    @classmethod
    def from_domain(
        cls, evaluation: InterventionEvaluation
    ) -> "InterventionEvaluationModel":
        return cls(
            id=evaluation.id,
            proposal_id=evaluation.proposal_id,
            outcome=evaluation.outcome.value,
            summary=evaluation.summary,
            findings=[
                {
                    "category": finding.category,
                    "description": finding.description,
                    "source": finding.source,
                    "confidence": finding.confidence,
                }
                for finding in evaluation.findings
            ],
            expected_benefits=list(evaluation.expected_benefits),
            potential_risks=list(evaluation.potential_risks),
            created_at=evaluation.created_at,
            correlation_id=evaluation.correlation_id,
        )

    def to_domain(self) -> InterventionEvaluation:
        return InterventionEvaluation(
            id=self.id,
            proposal_id=self.proposal_id,
            outcome=EvaluationOutcome(self.outcome),
            summary=self.summary,
            findings=[
                EvaluationFinding(
                    category=item["category"],
                    description=item["description"],
                    source=item["source"],
                    confidence=item["confidence"],
                )
                for item in self.findings
            ],
            expected_benefits=list(self.expected_benefits),
            potential_risks=list(self.potential_risks),
            created_at=self.created_at,
            correlation_id=self.correlation_id,
        )
