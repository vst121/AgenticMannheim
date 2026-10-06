from dataclasses import dataclass
from uuid import UUID

from agents.decision import AgentDecision
from policy.policy import PolicyDecision


@dataclass(frozen=True)
class AgentExecutionResult:
    run_id: UUID
    agent_decision: AgentDecision
    policy_decision: PolicyDecision