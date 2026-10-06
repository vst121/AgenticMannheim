from pydantic import BaseModel


class AgentExecutionResponse(BaseModel):
    executed: bool
    allowed: bool
    decision_type: str | None = None
    intersection_id: str | None = None
    reason: str