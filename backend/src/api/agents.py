from fastapi import APIRouter, Request

from agents.emergency_agent import EmergencyAgent
from agents.orchestrator import AgentOrchestrator
from decision.executor import DecisionExecutor
from decision.translator import DecisionTranslator
from digital_twin.twin import DigitalTwin
from policy.policy import CityPolicy
from simulation.engine import SimulationEngine

router = APIRouter(prefix="/api/agents", tags=["Agents"])


@router.post("/emergency")
async def run_emergency_agent(request: Request) -> dict[str, bool]:
    digital_twin: DigitalTwin = request.app.state.digital_twin

    agent = EmergencyAgent(digital_twin)
    translator = DecisionTranslator()
    policy = CityPolicy()
    simulation = SimulationEngine(digital_twin)
    executor = DecisionExecutor(policy, simulation)

    orchestrator = AgentOrchestrator(
        agent=agent,
        translator=translator,
        executor=executor,
    )

    executed = orchestrator.run()

    return {"executed": executed}