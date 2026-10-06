from uuid import UUID

from domain.event import CityEvent, CityEventType
from infrastructure.persistence.repositories.event_repository import EventRepository
from policy.policy import CityPolicy, PolicyDecision
from simulation.actions import SimulationAction
from simulation.engine import SimulationEngine


class DecisionExecutor:
    def __init__(
        self,
        policy: CityPolicy,
        simulation: SimulationEngine,
        event_repository: EventRepository,
    ) -> None:
        self._policy = policy
        self._simulation = simulation
        self._event_repository = event_repository

    def execute(
        self,
        action: SimulationAction,
        run_id: UUID,
    ) -> PolicyDecision:
        decision = self._policy.validate(action)

        if not decision.allowed:
            self._event_repository.add(
                CityEvent(
                    event_type=CityEventType.POLICY_REJECTED_ACTION,
                    aggregate_id=action.intersection_id,
                    correlation_id=run_id,
                    payload={
                        "action_type": action.action_type.value,
                        "reason": decision.reason,
                        "traffic_light_state": action.traffic_light_state,
                    },
                )
            )

            return decision

        self._simulation.execute(
            action=action,
            run_id=run_id,
        )

        return decision