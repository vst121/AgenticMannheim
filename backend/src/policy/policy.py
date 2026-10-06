from dataclasses import dataclass

from digital_twin.twin import DigitalTwin
from simulation.actions import SimulationAction


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


class CityPolicy:
    def __init__(self, digital_twin: DigitalTwin) -> None:
        self._digital_twin = digital_twin

    def validate(self, action: SimulationAction) -> PolicyDecision:
        allowed_states = {"red", "yellow", "green"}

        if action.traffic_light_state not in allowed_states:
            return PolicyDecision(
                allowed=False,
                reason=(
                    f"Traffic light state "
                    f"'{action.traffic_light_state}' is not allowed."
                ),
            )

        intersection = next(
            (
                intersection
                for intersection in self._digital_twin.get_state().intersections
                if intersection.id == action.intersection_id
            ),
            None,
        )

        if intersection is None:
            return PolicyDecision(
                allowed=False,
                reason="Target intersection does not exist.",
            )

        if intersection.traffic_light.value == action.traffic_light_state:
            return PolicyDecision(
                allowed=False,
                reason=(
                    f"Traffic light is already "
                    f"'{action.traffic_light_state}'."
                ),
            )

        return PolicyDecision(
            allowed=True,
            reason="Action is allowed.",
        )