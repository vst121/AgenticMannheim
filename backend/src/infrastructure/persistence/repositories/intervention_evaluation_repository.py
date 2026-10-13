from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.intervention_evaluation import InterventionEvaluation
from infrastructure.persistence.models.intervention_evaluation import (
    InterventionEvaluationModel,
)


class InterventionEvaluationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self, evaluation: InterventionEvaluation
    ) -> InterventionEvaluation:
        model = InterventionEvaluationModel.from_domain(evaluation)
        self._session.add(model)
        self._session.flush()
        return model.to_domain()

    def get_by_id(
        self, evaluation_id: UUID
    ) -> InterventionEvaluation | None:
        model = self._session.get(
            InterventionEvaluationModel, evaluation_id
        )
        if model is None:
            return None
        return model.to_domain()

    def list_by_proposal(
        self, proposal_id: UUID
    ) -> list[InterventionEvaluation]:
        statement = (
            select(InterventionEvaluationModel)
            .where(
                InterventionEvaluationModel.proposal_id == proposal_id
            )
            .order_by(InterventionEvaluationModel.created_at.desc())
        )
        models = self._session.scalars(statement).all()
        return [model.to_domain() for model in models]
