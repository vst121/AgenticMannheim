from math import hypot

from agents.decision import AgentDecision, AgentDecisionType
from uuid import UUID
from digital_twin.twin import DigitalTwin
from domain.event import CityEvent, CityEventType
from domain.vehicle import VehicleType


class EmergencyAgent:
    def __init__(self, digital_twin: DigitalTwin) -> None:
        self._digital_twin = digital_twin

    def observe_and_decide(self) -> AgentDecision | None:
        state = self._digital_twin.get_state()

        emergency_vehicle = next(
            (
                vehicle
                for vehicle in state.vehicles
                if vehicle.type == VehicleType.EMERGENCY
            ),
            None,
        )

        if emergency_vehicle is None:
            return None

        intersection = self._find_target_intersection(emergency_vehicle)

        if intersection is None:
            return None

        return AgentDecision(
            decision_type=AgentDecisionType.PRIORITIZE_EMERGENCY,
            intersection_id=intersection.id,
            reason="Emergency vehicle is approaching the intersection.",
            vehicle_id=emergency_vehicle.id,
        )

    def _find_target_intersection(self, emergency_vehicle):
        intersections = self._digital_twin.get_state().intersections

        if not intersections:
            return None

        return min(
            intersections,
            key=lambda intersection: hypot(
                intersection.latitude - emergency_vehicle.latitude,
                intersection.longitude - emergency_vehicle.longitude,
            ),
        )

    def handle_event(self, event: CityEvent) -> AgentDecision | None:
        if event.event_type != CityEventType.VEHICLE_REACHED_INTERSECTION:
            return None

        vehicle_id = UUID(event.payload["vehicle_id"])
        intersection_id = UUID(str(event.aggregate_id))

        vehicle = next(
            (
                vehicle
                for vehicle in self._digital_twin.get_state().vehicles
                if vehicle.id == vehicle_id
            ),
            None,
        )

        if vehicle is None:
            return None

        if vehicle.type != VehicleType.EMERGENCY:
            return None

        return AgentDecision(
            decision_type=AgentDecisionType.PRIORITIZE_EMERGENCY,
            intersection_id=intersection_id,
            reason="Emergency vehicle reached the intersection.",
            vehicle_id=vehicle_id,
        )