from uuid import UUID

from agents.decision import AgentDecision
from agents.emergency_agent import EmergencyAgent
from agents.exceptions import AgentRunFailed
from agents.result import AgentExecutionResult
from agents.run import AgentRun, AgentRunStatus, AgentType
from decision.executor import DecisionExecutor
from decision.translator import DecisionTranslator
from domain.event import CityEvent, CityEventType
from infrastructure.persistence.repositories.event_repository import EventRepository

from infrastructure.persistence.repositories.agent_run_repository import (
    AgentRunRepository,
)

class AgentOrchestrator:
    def __init__(
        self,
        agent: EmergencyAgent,
        translator: DecisionTranslator,
        executor: DecisionExecutor,
        event_repository: EventRepository,
        agent_run_repository: AgentRunRepository,
    ) -> None:
        self._agent = agent
        self._translator = translator
        self._executor = executor
        self._event_repository = event_repository
        self._agent_run_repository = agent_run_repository

    def run(self) -> AgentExecutionResult:
        agent_run = AgentRun.start(
            agent_type=AgentType.EMERGENCY,
        )

        self._agent_run_repository.add(agent_run)

        try:
            decision = self._agent.observe_and_decide()

            if decision is None:
                agent_run = agent_run.complete()
                self._agent_run_repository.update(agent_run)

                return AgentExecutionResult(
                    run_id=agent_run.id,
                    status=agent_run.status,
                    agent_decision=None,
                    policy_decision=None,
                )

            self._record_decision(
                decision=decision,
                correlation_id=agent_run.id,
            )

            action = self._translator.translate(decision)

            policy_decision = self._executor.execute(
                action=action,
                run_id=agent_run.id,
            )

            if policy_decision.allowed:
                agent_run = agent_run.complete()
            else:
                agent_run = agent_run.reject()

            self._agent_run_repository.update(agent_run)

            return AgentExecutionResult(
                run_id=agent_run.id,
                status=agent_run.status,
                agent_decision=decision,
                policy_decision=policy_decision,
            )

        except Exception as exc:
            agent_run = agent_run.fail()

            raise AgentRunFailed(
                run=agent_run,
                cause=exc,
            ) from exc

    def handle_event(
        self,
        event: CityEvent,
    ) -> AgentExecutionResult | None:
        agent_run = AgentRun.start(
            agent_type=AgentType.EMERGENCY,
        )

        self._agent_run_repository.add(agent_run)

        try:
            decision = self._agent.handle_event(event)

            if decision is None:
                agent_run = agent_run.complete()
                self._agent_run_repository.update(agent_run)

                return None

            self._record_decision(
                decision=decision,
                correlation_id=agent_run.id,
            )

            action = self._translator.translate(decision)

            policy_decision = self._executor.execute(
                action=action,
                run_id=agent_run.id,
            )

            if policy_decision.allowed:
                agent_run = agent_run.complete()
            else:
                agent_run = agent_run.reject()

            self._agent_run_repository.update(agent_run)

            return AgentExecutionResult(
                run_id=agent_run.id,
                status=agent_run.status,
                agent_decision=decision,
                policy_decision=policy_decision,
            )

        except Exception as exc:
            agent_run = agent_run.fail()

            raise AgentRunFailed(
                run=agent_run,
                cause=exc,
            ) from exc

    def _record_decision(
        self,
        decision: AgentDecision,
        correlation_id: UUID,
    ) -> None:
        self._event_repository.add(
            CityEvent(
                event_type=CityEventType.AGENT_DECISION_PROPOSED,
                aggregate_id=decision.intersection_id,
                correlation_id=correlation_id,
                payload={
                    "decision_type": decision.decision_type.value,
                    "reason": decision.reason,
                    "intersection_id": str(decision.intersection_id),
                    "vehicle_id": str(decision.vehicle_id),
                },
            )
        )