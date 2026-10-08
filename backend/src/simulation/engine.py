import logging
from uuid import UUID

from domain.event import CityEvent, CityEventType
from domain.intersection import TrafficLightState
from domain.road import Road
from digital_twin.twin import DigitalTwin
from infrastructure.logging import configure_logging
from infrastructure.persistence.repositories.event_repository import (
    EventRepository,
)
from simulation.event_dispatcher import EventDispatcher
from simulation.state import SimulationState

from .actions import SimulationAction, SimulationActionType


configure_logging()

logger = logging.getLogger(__name__)


EMERGENCY_GREEN_DURATION_SECONDS = 3.0
EMERGENCY_YELLOW_DURATION_SECONDS = 2.0


class SimulationEngine:
    def __init__(
        self,
        digital_twin: DigitalTwin,
        event_repository: EventRepository,
        simulation_state: SimulationState,
        event_dispatcher: EventDispatcher,
    ) -> None:
        self._digital_twin = digital_twin
        self._event_repository = event_repository
        self._state = simulation_state
        self._event_dispatcher = event_dispatcher

        self._emergency_light_started_at: dict[UUID, float] = {}

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

    def change_traffic_light(
        self,
        intersection_id: UUID,
        state: TrafficLightState,
        emergency_priority: bool = False,
    ) -> None:
        intersection = next(
            (
                intersection
                for intersection in self._digital_twin.get_state().intersections
                if intersection.id == intersection_id
            ),
            None,
        )

        if intersection is None:
            raise ValueError(
                f"Intersection '{intersection_id}' was not found."
            )

        if intersection.traffic_light is None:
            raise ValueError(
                f"Intersection '{intersection_id}' "
                "does not have a traffic light."
            )

        previous_state = intersection.traffic_light

        intersection.traffic_light = state
        intersection.emergency_priority = emergency_priority

        print(
            "TRAFFIC LIGHT CHANGED:",
            f"intersection={intersection_id}",
            f"{previous_state.value} -> {state.value}",
            f"emergency_priority={emergency_priority}",
        )

    def tick(self, seconds: float = 1.0) -> None:
        self._state.advance(seconds)
        self._move_vehicles(seconds)
        self._update_emergency_traffic_lights()

    def _change_traffic_light(
        self,
        action: SimulationAction,
        correlation_id: UUID,
    ) -> None:
        try:
            traffic_light_state = TrafficLightState(
                action.traffic_light_state,
            )
        except ValueError as exc:
            raise ValueError(
                f"Invalid traffic light state: "
                f"{action.traffic_light_state}"
            ) from exc

        self._digital_twin.change_traffic_light(
            intersection_id=action.intersection_id,
            state=traffic_light_state,
            emergency_priority=True,
        )

        self._emergency_light_started_at[action.intersection_id] = (
            self._state.current_time.timestamp()
        )

        logger.info(
            "Traffic light changed by simulation: "
            "intersection_id=%s state=%s emergency_priority=%s",
            action.intersection_id,
            traffic_light_state.value,
            True,
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

    def _move_vehicles(self, seconds: float) -> None:
        twin_state = self._digital_twin.get_state()

        roads_by_id = {
            road.id: road
            for road in twin_state.roads
        }

        outgoing_roads_by_intersection: dict[UUID, list[Road]] = {}

        for road in twin_state.roads:
            outgoing_roads_by_intersection.setdefault(
                road.start_intersection_id,
                [],
            ).append(road)

        for vehicle in twin_state.vehicles:
            if vehicle.road_id is None:
                continue

            if vehicle.speed_kmh <= 0:
                continue

            remaining_distance = (
                vehicle.speed_kmh * 1000 / 3600
            ) * seconds

            while remaining_distance > 0:
                road = roads_by_id.get(vehicle.road_id)

                if road is None:
                    break

                distance_to_end = (
                    road.length_meters
                    - vehicle.position_on_road_meters
                )

                if remaining_distance < distance_to_end:
                    vehicle.position_on_road_meters += (
                        remaining_distance
                    )

                    remaining_distance = 0

                    latitude, longitude = self._position_on_road(
                        road=road,
                        position_meters=vehicle.position_on_road_meters,
                    )

                    vehicle.latitude = latitude
                    vehicle.longitude = longitude

                    continue

                # Vehicle reached the end of the current road.
                remaining_distance -= distance_to_end

                vehicle.position_on_road_meters = (
                    road.length_meters
                )

                latitude, longitude = self._position_on_road(
                    road=road,
                    position_meters=road.length_meters,
                )

                vehicle.latitude = latitude
                vehicle.longitude = longitude

                event = CityEvent(
                    event_type=CityEventType.VEHICLE_REACHED_INTERSECTION,
                    aggregate_id=road.end_intersection_id,
                    payload={
                        "vehicle_id": str(vehicle.id),
                        "road_id": str(road.id),
                    },
                )

                self._event_repository.add(event)

                logger.info(
                    "Vehicle reached intersection: "
                    "vehicle_id=%s intersection_id=%s",
                    vehicle.id,
                    road.end_intersection_id,
                )

                self._event_dispatcher.dispatch(event)

                # Find roads leaving the current intersection.
                outgoing_roads = outgoing_roads_by_intersection.get(
                    road.end_intersection_id,
                    [],
                )

                if not outgoing_roads:
                    # There is nowhere else to go.
                    vehicle.speed_kmh = 0.0
                    break

                # For now, choose one connected outgoing road.
                next_road = next(
                    (
                        candidate
                        for candidate in outgoing_roads
                        if candidate.id != road.id
                    ),
                    None,
                )

                if next_road is None:
                    vehicle.speed_kmh = 0.0
                    break

                vehicle.road_id = next_road.id
                vehicle.position_on_road_meters = 0.0

                latitude, longitude = self._position_on_road(
                    road=next_road,
                    position_meters=0.0,
                )

                vehicle.latitude = latitude
                vehicle.longitude = longitude

    def _update_emergency_traffic_lights(self) -> None:
        twin_state = self._digital_twin.get_state()
        current_timestamp = self._state.current_time.timestamp()

        for intersection in twin_state.intersections:
            if not intersection.emergency_priority:
                continue

            started_at = self._emergency_light_started_at.get(
                intersection.id
            )

            if started_at is None:
                continue

            elapsed = current_timestamp - started_at

            if (
                intersection.traffic_light
                == TrafficLightState.GREEN
                and elapsed >= EMERGENCY_GREEN_DURATION_SECONDS
            ):
                intersection.traffic_light = TrafficLightState.YELLOW

                logger.info(
                    "Emergency green phase ended: "
                    "intersection_id=%s state=yellow elapsed=%.1fs",
                    intersection.id,
                    elapsed,
                )

                continue

            if (
                intersection.traffic_light
                == TrafficLightState.YELLOW
                and elapsed
                >= (
                    EMERGENCY_GREEN_DURATION_SECONDS
                    + EMERGENCY_YELLOW_DURATION_SECONDS
                )
            ):
                intersection.traffic_light = TrafficLightState.RED
                intersection.emergency_priority = False

                self._emergency_light_started_at.pop(
                    intersection.id,
                    None,
                )

                logger.info(
                    "Emergency priority ended: "
                    "intersection_id=%s state=red elapsed=%.1fs",
                    intersection.id,
                    elapsed,
                )

    def _position_on_road(
        self,
        road,
        position_meters: float,
    ) -> tuple[float, float]:
        geometry = road.geometry

        if not geometry:
            raise ValueError(
                f"Road '{road.id}' has no geometry."
            )

        if len(geometry) == 1:
            return (
                geometry[0].latitude,
                geometry[0].longitude,
            )

        remaining = position_meters

        for first, second in zip(
            geometry,
            geometry[1:],
        ):
            segment_length = self._distance_meters(
                first.latitude,
                first.longitude,
                second.latitude,
                second.longitude,
            )

            if remaining <= segment_length:
                ratio = (
                    remaining / segment_length
                    if segment_length > 0
                    else 0.0
                )

                latitude = (
                    first.latitude
                    + (
                        second.latitude
                        - first.latitude
                    ) * ratio
                )

                longitude = (
                    first.longitude
                    + (
                        second.longitude
                        - first.longitude
                    ) * ratio
                )

                return latitude, longitude

            remaining -= segment_length

        last = geometry[-1]

        return last.latitude, last.longitude

    @staticmethod
    def _distance_meters(
        latitude1: float,
        longitude1: float,
        latitude2: float,
        longitude2: float,
    ) -> float:
        latitude_distance = (
            latitude2 - latitude1
        ) * 111_000

        longitude_distance = (
            longitude2 - longitude1
        ) * 111_000

        return (
            latitude_distance**2
            + longitude_distance**2
        ) ** 0.5

    @property
    def state(self) -> SimulationState:
        return self._state