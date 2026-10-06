from domain.intersection import TrafficLightState
from digital_twin.twin import DigitalTwin

from .actions import SimulationAction, SimulationActionType


class SimulationEngine:
    def __init__(self, digital_twin: DigitalTwin) -> None:
        self._digital_twin = digital_twin

    def execute(self, action: SimulationAction) -> None:
        if action.action_type == SimulationActionType.CHANGE_TRAFFIC_LIGHT:
            self._change_traffic_light(action)
            return

        raise ValueError(
            f"Unsupported simulation action: {action.action_type}"
        )

    def _change_traffic_light(self, action: SimulationAction) -> None:
        try:
            traffic_light_state = TrafficLightState(
                action.traffic_light_state
            )
        except ValueError as exc:
            raise ValueError(
                f"Invalid traffic light state: "
                f"{action.traffic_light_state}"
            ) from exc

        self._digital_twin.change_traffic_light(
            intersection_id=action.intersection_id,
            state=traffic_light_state,
        )