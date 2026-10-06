from pydantic import BaseModel


class AgentExecutionResponse(BaseModel):
    executed: bool
    allowed: bool
    reason: str