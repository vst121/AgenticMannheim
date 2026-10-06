from fastapi import APIRouter, HTTPException, Request

from agents.emergency_agent import EmergencyAgent
from agents.exceptions import AgentRunFailed
from agents.orchestrator import AgentOrchestrator
from api.schemas import AgentExecutionResponse
from decision.executor import DecisionExecutor
from decision.translator import DecisionTranslator
from digital_twin.twin import DigitalTwin
from domain.event import CityEvent, CityEventType
from infrastructure.persistence.database import SessionLocal
from infrastructure.persistence.repositories.event_repository import EventRepository
from policy.policy import CityPolicy
from simulation.engine import SimulationEngine
from infrastructure.persistence.repositories.agent_run_repository import (
    AgentRunRepository,
)

router = APIRouter(
    prefix="/api/agents",
    tags=["Agents"],
)


@router.post(
    "/emergency",
    response_model=AgentExecutionResponse,
)
async def run_emergency_agent(
    request: Request,
) -> AgentExecutionResponse:
    digital_twin: DigitalTwin = request.app.state.digital_twin

    agent = EmergencyAgent(digital_twin)
    translator = DecisionTranslator()
    policy = CityPolicy(digital_twin)

    try:
        with SessionLocal() as session:
            event_repository = EventRepository(session)
            agent_run_repository = AgentRunRepository(session)

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
                agent_run_repository=agent_run_repository,
            )

            result = orchestrator.run()

            session.commit()

    except AgentRunFailed as exc:
        with SessionLocal() as audit_session:
            event_repository = EventRepository(audit_session)
            agent_run_repository = AgentRunRepository(audit_session)

            agent_run_repository.add(exc.run)

            event_repository.add(
                CityEvent(
                    event_type=CityEventType.AGENT_RUN_FAILED,
                    correlation_id=exc.run.id,
                    payload={
                        "error_type": type(exc.cause).__name__,
                        "error": str(exc.cause),
                    },
                )
            )

            audit_session.commit()

        raise HTTPException(
            status_code=500,
            detail={
                "run_id": str(exc.run_id),
                "message": "Agent execution failed.",
            },
        ) from exc.cause

    if result.agent_decision is None:
        return AgentExecutionResponse(
            run_id=str(result.run_id),
            status=result.status.value,
            executed=False,
            allowed=False,
            reason="No emergency vehicle requiring action was found.",
        )

    return AgentExecutionResponse(
        run_id=str(result.run_id),
        status=result.status.value,
        executed=result.policy_decision.allowed,
        allowed=result.policy_decision.allowed,
        decision_type=result.agent_decision.decision_type.value,
        intersection_id=str(result.agent_decision.intersection_id),
        reason=result.agent_decision.reason,
    )