from uuid import UUID

from domain.event import CityEvent, CityEventType
from domain.intersection import TrafficLightState
from digital_twin.twin import DigitalTwin
from infrastructure.persistence.repositories.event_repository import EventRepository

from .actions import SimulationAction, SimulationActionType


class SimulationEngine:
    def __init__(
        self,
        digital_twin: DigitalTwin,
        event_repository: EventRepository,
    ) -> None:
        self._digital_twin = digital_twin
        self._event_repository = event_repository

    def execute(
        self,
        action: SimulationAction,
        run_id: UUID,
    ) -> None:
        if action.action_type == SimulationActionType.CHANGE_TRAFFIC_LIGHT:
            self._change_traffic_light(
                action=action,
                correlation_id=run_id,
            )
            return

        raise ValueError(
            f"Unsupported simulation action: {action.action_type}"
        )

    def _change_traffic_light(
        self,
        action: SimulationAction,
        correlation_id: UUID,
    ) -> None:
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

        self._event_repository.add(
            CityEvent(
                event_type=CityEventType.TRAFFIC_LIGHT_CHANGED,
                aggregate_id=action.intersection_id,
                correlation_id=correlation_id,
                payload={
                    "traffic_light_state": traffic_light_state.value,
                    "vehicle_id": str(action.vehicle_id),
                },
            )
        )