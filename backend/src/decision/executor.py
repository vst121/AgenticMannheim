from policy.policy import CityPolicy
from simulation.actions import SimulationAction
from simulation.engine import SimulationEngine


class DecisionExecutor:
    def __init__(
        self,
        policy: CityPolicy,
        simulation: SimulationEngine,
    ) -> None:
        self._policy = policy
        self._simulation = simulation

    def execute(self, action: SimulationAction) -> None:
        decision = self._policy.validate(action)

        if not decision.allowed:
            raise PermissionError(decision.reason)

        self._simulation.execute(action)