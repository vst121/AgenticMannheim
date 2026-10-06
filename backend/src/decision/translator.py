from domain.intersection import TrafficLightState
from agents.decision import AgentDecision, AgentDecisionType
from simulation.actions import (
    SimulationAction,
    SimulationActionType,
)


class DecisionTranslator:
    def translate(
        self,
        decision: AgentDecision,
    ) -> SimulationAction:
        if decision.decision_type == AgentDecisionType.PRIORITIZE_EMERGENCY:
            return SimulationAction(
                action_type=SimulationActionType.CHANGE_TRAFFIC_LIGHT,
                intersection_id=decision.intersection_id,
                traffic_light_state=TrafficLightState.GREEN.value,
            )

        raise ValueError(
            f"Unsupported agent decision: {decision.decision_type}"
        )