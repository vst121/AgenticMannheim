import asyncio
from uuid import UUID
import logging
from domain.event import CityEvent, CityEventType
from domain.intersection import TrafficLightState
from digital_twin.twin import DigitalTwin
from infrastructure.persistence.repositories.event_repository import (
    EventRepository,
)
from simulation.event_dispatcher import EventDispatcher
from simulation.state import SimulationState

from .actions import SimulationAction, SimulationActionType
from infrastructure.logging import configure_logging

configure_logging()

logger = logging.getLogger(__name__)

class SimulationEngine:
    def __init__(
        self,
        digital_twin: DigitalTwin,
        event_repository: EventRepository,
        simulation_state: SimulationState,
        event_dispatcher: EventDispatcher
    ) -> None:
        self._digital_twin = digital_twin
        self._event_repository = event_repository
        self._state = simulation_state
        self._event_dispatcher = event_dispatcher

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

            latitude, longitude = self._position_on_road(
                road=road,
                position_meters=vehicle.position_on_road_meters,
            )

            vehicle.latitude = latitude
            vehicle.longitude = longitude

            if (
                previous_position < road.length_meters
                and vehicle.position_on_road_meters >= road.length_meters
            ):
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
                    "Vehicle reached intersection: vehicle_id=%s intersection_id=%s",
                    vehicle.id,
                    road.end_intersection_id,
                )

                self._event_dispatcher.dispatch(event)

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