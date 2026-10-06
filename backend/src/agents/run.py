from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4


class AgentType(StrEnum):
    EMERGENCY = "emergency"


class AgentRunStatus(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    REJECTED = "rejected"
    FAILED = "failed"


@dataclass(frozen=True)
class AgentRun:
    id: UUID
    agent_type: AgentType
    status: AgentRunStatus
    started_at: datetime
    completed_at: datetime | None = None

    @classmethod
    def start(cls, agent_type: AgentType) -> "AgentRun":
        return cls(
            id=uuid4(),
            agent_type=agent_type,
            status=AgentRunStatus.STARTED,
            started_at=datetime.now(timezone.utc),
        )

    def complete(self) -> "AgentRun":
        return AgentRun(
            id=self.id,
            agent_type=self.agent_type,
            status=AgentRunStatus.COMPLETED,
            started_at=self.started_at,
            completed_at=datetime.now(timezone.utc),
        )

    def reject(self) -> "AgentRun":
        return AgentRun(
            id=self.id,
            agent_type=self.agent_type,
            status=AgentRunStatus.REJECTED,
            started_at=self.started_at,
            completed_at=datetime.now(timezone.utc),
        )

    def fail(self) -> "AgentRun":
        return AgentRun(
            id=self.id,
            agent_type=self.agent_type,
            status=AgentRunStatus.FAILED,
            started_at=self.started_at,
            completed_at=datetime.now(timezone.utc),
        )