from fastapi import APIRouter, Request

from digital_twin.twin import DigitalTwin

from agents.emergency_agent import EmergencyAgent
from agents.orchestrator import AgentOrchestrator
from decision.executor import DecisionExecutor
from decision.translator import DecisionTranslator
from policy.policy import CityPolicy
from simulation.engine import SimulationEngine

router = APIRouter(prefix="/api/city", tags=["City"])


@router.get("/state")
async def get_city_state(request: Request):
    digital_twin: DigitalTwin = request.app.state.digital_twin
    state = digital_twin.get_state()

    return {
        "city": {
            "name": state.city.name,
            "area": state.city.area,
            "latitude": state.city.latitude,
            "longitude": state.city.longitude,
        },
        "roads": [
            {
                "id": str(road.id),
                "name": road.name,
                "road_type": road.road_type.value,
                "length_meters": road.length_meters,
                "speed_limit_kmh": road.speed_limit_kmh,
                "lanes": road.lanes,
            }
            for road in state.roads
        ],
        "vehicles": [
            {
                "id": str(vehicle.id),
                "type": vehicle.type.value,
                "latitude": vehicle.latitude,
                "longitude": vehicle.longitude,
                "speed_kmh": vehicle.speed_kmh,
            }
            for vehicle in state.vehicles
        ],        
        "intersections": [
            {
                "id": str(intersection.id),
                "name": intersection.name,
                "latitude": intersection.latitude,
                "longitude": intersection.longitude,
                "traffic_light": intersection.traffic_light.value,
            }
            for intersection in state.intersections
        ],
    }
