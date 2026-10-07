import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    with SessionLocal() as session:
        loader = DigitalTwinLoader(session)
        app.state.digital_twin = loader.load()

    app.state.simulation_state = SimulationState.create()

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
                    )

                    simulation.tick(1.0)

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
