from uuid import UUID

from agents.decision import AgentDecision, AgentDecisionType
from digital_twin.twin import DigitalTwin
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
            reason=(
                "Emergency vehicle is approaching the intersection."
            ),
        )

    def _find_target_intersection(self, vehicle):
        if not self._digital_twin.get_state().intersections:
            return None

        return self._digital_twin.get_state().intersections[0]