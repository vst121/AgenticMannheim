import asyncio
from contextlib import asynccontextmanager
from agents.emergency_agent import EmergencyAgent
from agents.exceptions import AgentRunFailed
from agents.orchestrator import AgentOrchestrator
from decision.executor import DecisionExecutor
from decision.translator import DecisionTranslator
from domain.event import CityEvent, CityEventType
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from infrastructure.logging import configure_logging
from infrastructure.persistence.repositories.agent_run_repository import AgentRunRepository
from policy.policy import CityPolicy
from simulation.event_dispatcher import EventDispatcher

from api.agents import router as agents_router
from api.city import router as city_router
from api.intersections import router as intersections_router
from api.roads import router as roads_router
from api.scenarios import router as scenarios_router
from api.simulation import router as simulation_router
from api.vehicles import router as vehicles_router
from digital_twin.loader import DigitalTwinLoader
from infrastructure.persistence.database import SessionLocal
from infrastructure.persistence.repositories.event_repository import EventRepository
from simulation.engine import SimulationEngine
from simulation.state import SimulationState

configure_logging()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    with SessionLocal() as session:
        loader = DigitalTwinLoader(session)
        app.state.digital_twin = loader.load()

    app.state.simulation_state = SimulationState.create()
    app.state.event_dispatcher = EventDispatcher()
    emergency_agent = EmergencyAgent(
        app.state.digital_twin,
    )

    decision_translator = DecisionTranslator()
    city_policy = CityPolicy(
        app.state.digital_twin,
    )

    # ✅ Define the handler FIRST
    def handle_city_event(event: CityEvent) -> None:
        try:
            with SessionLocal() as session:
                event_repository = EventRepository(session)
                agent_run_repository = AgentRunRepository(session)

                simulation = SimulationEngine(
                    digital_twin=app.state.digital_twin,
                    event_repository=event_repository,
                    simulation_state=app.state.simulation_state,
                    event_dispatcher=app.state.event_dispatcher,
                )

                translator = DecisionTranslator()

                policy = CityPolicy(
                    app.state.digital_twin,
                )

                executor = DecisionExecutor(
                    policy=policy,
                    simulation=simulation,
                    event_repository=event_repository,
                )

                orchestrator = AgentOrchestrator(
                    agent=emergency_agent,
                    translator=translator,
                    executor=executor,
                    event_repository=event_repository,
                    agent_run_repository=agent_run_repository,
                )

                orchestrator.handle_event(event)

                session.commit()

        except AgentRunFailed as exc:
            with SessionLocal() as session:
                event_repository = EventRepository(session)
                agent_run_repository = AgentRunRepository(session)

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

                session.commit()

            logger.exception(
                "Agent run failed: run_id=%s",
                exc.run_id,
            )

    app.state.event_dispatcher.subscribe(
        CityEventType.VEHICLE_REACHED_INTERSECTION.value,
        handle_city_event,
    )

    async def simulation_loop() -> None:
        while True:
            try:
                await asyncio.sleep(1.0)

                with SessionLocal() as session:
                    event_repository = EventRepository(session)

                    simulation = SimulationEngine(
                        digital_twin=app.state.digital_twin,
                        event_repository=event_repository,
                        simulation_state=app.state.simulation_state,
                        event_dispatcher=app.state.event_dispatcher
                    )

                    simulation.tick(1.0)

                    # logger.info(
                    #     "Digital Twin loaded: %s intersections, %s roads",
                    #     len(app.state.digital_twin.get_state().intersections),
                    #     len(app.state.digital_twin.get_state().roads),
                    # )

                    session.commit()

            except asyncio.CancelledError:
                raise

            except Exception:
                import traceback

                traceback.print_exc()

    simulation_task = asyncio.create_task(simulation_loop())

    try:
        yield
    finally:
        simulation_task.cancel()

        try:
            await simulation_task
        except asyncio.CancelledError:
            pass
        

app = FastAPI(
    title="Agentic Mannheim",
    description="Experimental Agentic Digital Twin of Mannheim",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(city_router)
app.include_router(agents_router)
app.include_router(roads_router)
app.include_router(intersections_router)
app.include_router(vehicles_router)
app.include_router(scenarios_router)
app.include_router(simulation_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
