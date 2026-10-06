from dataclasses import dataclass
from uuid import UUID

from agents.decision import AgentDecision
from agents.run import AgentRunStatus
from policy.policy import PolicyDecision


@dataclass(frozen=True)
class AgentExecutionResult:
    run_id: UUID
    status: AgentRunStatus
    agent_decision: AgentDecision
    policy_decision: PolicyDecision