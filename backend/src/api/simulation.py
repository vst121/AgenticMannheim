from fastapi import APIRouter, Request
from pydantic import BaseModel


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
    simulation = request.app.state.simulation

    simulation.tick(body.seconds)

    state = simulation.state

    return SimulationTickResponse(
        tick=state.tick,
        current_time=state.current_time.isoformat(),
    )