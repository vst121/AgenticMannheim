import digital_twin
from fastapi import APIRouter, Request

from agents.emergency_agent import EmergencyAgent
from agents.orchestrator import AgentOrchestrator
from decision.executor import DecisionExecutor
from decision.translator import DecisionTranslator
from digital_twin.twin import DigitalTwin
from infrastructure.persistence.database import SessionLocal
from infrastructure.persistence.repositories import event_repository
from infrastructure.persistence.repositories.event_repository import EventRepository
from policy.policy import CityPolicy
from simulation.engine import SimulationEngine

router = APIRouter(prefix="/api/agents", tags=["Agents"])


@router.post("/emergency")
async def run_emergency_agent(request: Request) -> dict[str, bool]:
    digital_twin: DigitalTwin = request.app.state.digital_twin

    agent = EmergencyAgent(digital_twin)
    translator = DecisionTranslator()
    policy = CityPolicy(digital_twin)

    with SessionLocal() as session:
        event_repository = EventRepository(session)

        simulation = SimulationEngine(
            digital_twin=digital_twin,
            event_repository=event_repository,
        )

        executor = DecisionExecutor(
            policy=policy,            
            simulation=simulation,
            event_repository=event_repository,
        )

        orchestrator = AgentOrchestrator(
            agent=agent,
            translator=translator,
            executor=executor,
            event_repository=event_repository,
        )

        executed = orchestrator.run()

        session.commit()

    return {"executed": executed}