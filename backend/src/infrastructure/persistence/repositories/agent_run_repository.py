from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from agents.run import AgentRun, AgentRunStatus, AgentType
from ..models.agent_run import AgentRunModel


class AgentRunRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, run_id: UUID) -> AgentRun | None:
        statement = select(AgentRunModel).where(
            AgentRunModel.id == run_id
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def add(self, run: AgentRun) -> AgentRun:
        model = self._to_model(run)

        self._session.add(model)
        self._session.flush()

        return self._to_domain(model)

    def update(self, run: AgentRun) -> AgentRun:
        model = self._session.get(
            AgentRunModel,
            run.id,
        )

        if model is None:
            raise ValueError(
                f"Agent run '{run.id}' was not found."
            )

        model.agent_type = run.agent_type
        model.status = run.status.value
        model.started_at = run.started_at
        model.completed_at = run.completed_at

        self._session.flush()

        return self._to_domain(model)

    @staticmethod
    def _to_domain(model: AgentRunModel) -> AgentRun:
        return AgentRun(
            id=model.id,
            agent_type=AgentType(model.agent_type),
            status=AgentRunStatus(model.status),
            started_at=model.started_at,
            completed_at=model.completed_at,
        )

    @staticmethod
    def _to_model(run: AgentRun) -> AgentRunModel:
        return AgentRunModel(
            id=run.id,
            agent_type=run.agent_type.value,
            status=run.status.value,
            started_at=run.started_at,
            completed_at=run.completed_at,
        )