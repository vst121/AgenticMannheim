from fastapi import FastAPI

app = FastAPI(
    title="Agentic Mannheim",
    description="Experimental Agentic Digital Twin of Mannheim",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}