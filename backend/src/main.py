from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from digital_twin.loader import DigitalTwinLoader
from infrastructure.persistence.database import SessionLocal

from api.city import router as city_router
from api.agents import router as agents_router
from api.roads import router as roads_router
from api.intersections import router as intersections_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    with SessionLocal() as session:
        loader = DigitalTwinLoader(session)
        app.state.digital_twin = loader.load()

    yield


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

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}