from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1.city import router as city_router
from infrastructure.persistence.init_db import initialize_database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    initialize_database()

    yield


app = FastAPI(
    title="Agentic Mannheim",
    description="Experimental Agentic Digital Twin of Mannheim",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(city_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}