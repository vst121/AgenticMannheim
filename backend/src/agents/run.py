from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID, uuid4


class AgentRunStatus(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    REJECTED = "rejected"
    FAILED = "failed"


@dataclass(frozen=True)
class AgentRun:
    id: UUID
    status: AgentRunStatus

    @classmethod
    def start(cls) -> "AgentRun":
        return cls(
            id=uuid4(),
            status=AgentRunStatus.STARTED,
        )

    def complete(self) -> "AgentRun":
        return AgentRun(
            id=self.id,
            status=AgentRunStatus.COMPLETED,
        )

    def reject(self) -> "AgentRun":
        return AgentRun(
            id=self.id,
            status=AgentRunStatus.REJECTED,
        )

    def fail(self) -> "AgentRun":
        return AgentRun(
            id=self.id,
            status=AgentRunStatus.FAILED,
        )