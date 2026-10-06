from agents.decision import AgentDecision
from agents.emergency_agent import EmergencyAgent
from agents.result import AgentExecutionResult
from decision.executor import DecisionExecutor
from decision.translator import DecisionTranslator
from domain.event import CityEvent, CityEventType
from infrastructure.persistence.repositories.event_repository import EventRepository
from policy.policy import PolicyDecision


class AgentOrchestrator:
    def __init__(
        self,
        agent: EmergencyAgent,
        translator: DecisionTranslator,
        executor: DecisionExecutor,
        event_repository: EventRepository,
    ) -> None:
        self._agent = agent
        self._translator = translator
        self._executor = executor
        self._event_repository = event_repository

    def run(self) -> AgentExecutionResult | None:
        decision = self._agent.observe_and_decide()

        if decision is None:
            return None

        self._record_decision(decision)

        action = self._translator.translate(decision)

        policy_decision = self._executor.execute(action)

        return AgentExecutionResult(
            agent_decision=decision,
            policy_decision=policy_decision,
        )

    def _record_decision(self, decision: AgentDecision) -> None:
        event = CityEvent(
            event_type=CityEventType.AGENT_DECISION_PROPOSED,
            aggregate_id=decision.intersection_id,
            payload={
                "decision_type": decision.decision_type.value,
                "reason": decision.reason,
                "intersection_id": str(decision.intersection_id),
                "vehicle_id": str(decision.vehicle_id),
            },
        )

        self._event_repository.add(event)