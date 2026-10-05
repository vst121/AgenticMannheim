from fastapi import FastAPI

from api.v1.city import router as city_router


app = FastAPI(
    title="Agentic Mannheim",
    description="Experimental Agentic Digital Twin of Mannheim",
    version="0.1.0",
)

app.include_router(city_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}