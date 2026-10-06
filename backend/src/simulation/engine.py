from uuid import UUID

from domain.event import CityEvent, CityEventType
from domain.intersection import TrafficLightState
from digital_twin.twin import DigitalTwin
from infrastructure.persistence.repositories.event_repository import EventRepository
from simulation.state import SimulationState

from .actions import SimulationAction, SimulationActionType


class SimulationEngine:
    def __init__(
        self,
        digital_twin: DigitalTwin,
        event_repository: EventRepository,
        simulation_state: SimulationState,
    ) -> None:
        self._digital_twin = digital_twin
        self._event_repository = event_repository
        self._state = simulation_state

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

    def tick(self, seconds: float = 1.0) -> None:
        self._state.advance(seconds)

        self._move_vehicles(seconds)        

    def _move_vehicles(self, seconds: float) -> None:
        twin_state = self._digital_twin.get_state()

        roads_by_id = {
            road.id: road
            for road in twin_state.roads
        }

        for vehicle in twin_state.vehicles:
            if vehicle.road_id is None:
                continue

            if vehicle.speed_kmh <= 0:
                continue

            road = roads_by_id.get(vehicle.road_id)

            if road is None:
                continue

            distance_meters = (
                vehicle.speed_kmh * 1000 / 3600
            ) * seconds

            previous_position = vehicle.position_on_road_meters

            vehicle.position_on_road_meters = min(
                vehicle.position_on_road_meters + distance_meters,
                road.length_meters,
            )

            if (
                previous_position < road.length_meters
                and vehicle.position_on_road_meters >= road.length_meters
            ):
                self._event_repository.add(
                    CityEvent(
                        event_type=CityEventType.VEHICLE_REACHED_INTERSECTION,
                        aggregate_id=road.end_intersection_id,
                        payload={
                            "vehicle_id": str(vehicle.id),
                            "road_id": str(road.id),
                        },
                    )
                )