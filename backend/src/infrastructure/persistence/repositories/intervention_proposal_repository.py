from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.intervention_proposal import InterventionProposal
from infrastructure.persistence.models.intervention_proposal import (
    InterventionProposalModel,
)


class InterventionProposalRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, proposal: InterventionProposal) -> InterventionProposal:
        model = InterventionProposalModel.from_domain(proposal)
        self._session.add(model)
        self._session.flush()
        return model.to_domain()

    def get_by_id(self, proposal_id: UUID) -> InterventionProposal | None:
        model = self._session.get(InterventionProposalModel, proposal_id)
        if model is None:
            return None
        return model.to_domain()

    def list_by_request(
        self,
        request_id: UUID,
    ) -> list[InterventionProposal]:
        statement = (
            select(InterventionProposalModel)
            .where(InterventionProposalModel.request_id == request_id)
            .order_by(InterventionProposalModel.created_at.desc())
        )
        models = self._session.scalars(statement).all()
        return [model.to_domain() for model in models]

    def update(self, proposal: InterventionProposal) -> InterventionProposal:
        model = self._session.get(InterventionProposalModel, proposal.id)
        if model is None:
            raise ValueError(
                f"Intervention proposal '{proposal.id}' was not found."
            )

        updated_model = InterventionProposalModel.from_domain(proposal)

        model.request_id = updated_model.request_id
        model.investigation_id = updated_model.investigation_id
        model.intervention_type = updated_model.intervention_type
        model.title = updated_model.title
        model.description = updated_model.description
        model.target_intersection_id = updated_model.target_intersection_id
        model.expected_benefits = updated_model.expected_benefits
        model.potential_risks = updated_model.potential_risks
        model.status = updated_model.status
        model.created_at = updated_model.created_at
        model.correlation_id = updated_model.correlation_id

        self._session.flush()
        return model.to_domain()
