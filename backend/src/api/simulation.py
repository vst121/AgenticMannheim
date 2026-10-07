from fastapi import APIRouter, Request
from pydantic import BaseModel

from infrastructure.persistence.database import SessionLocal
from infrastructure.persistence.repositories.event_repository import (
    EventRepository,
)
from simulation.engine import SimulationEngine


class SimulationTickRequest(BaseModel):
    seconds: float = 1.0


class SimulationTickResponse(BaseModel):
    tick: int
    current_time: str


router = APIRouter(
    prefix="/api/simulation",
    tags=["Simulation"],
)


@router.post(
    "/tick",
    response_model=SimulationTickResponse,
)
async def simulation_tick(
    request: Request,
    body: SimulationTickRequest,
) -> SimulationTickResponse:
    digital_twin = request.app.state.digital_twin
    simulation_state = request.app.state.simulation_state

    with SessionLocal() as session:
        event_repository = EventRepository(session)

        simulation = SimulationEngine(
            digital_twin=digital_twin,
            event_repository=event_repository,
            simulation_state=simulation_state,
        )

        simulation.tick(body.seconds)

        session.commit()

    return SimulationTickResponse(
        tick=simulation_state.tick,
        current_time=simulation_state.current_time.isoformat(),
    )
