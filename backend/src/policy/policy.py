from dataclasses import dataclass

from simulation.actions import SimulationAction


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


class CityPolicy:
    def validate(
        self,
        action: SimulationAction,
    ) -> PolicyDecision:
        if not action.traffic_light_state:
            return PolicyDecision(
                allowed=False,
                reason="Traffic light state is required.",
            )

        allowed_states = {"red", "yellow", "green"}

        if action.traffic_light_state not in allowed_states:
            return PolicyDecision(
                allowed=False,
                reason=(
                    f"Traffic light state "
                    f"'{action.traffic_light_state}' is not allowed."
                ),
            )

        return PolicyDecision(
            allowed=True,
            reason="Action is allowed.",
        )