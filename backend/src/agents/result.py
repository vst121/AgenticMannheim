from dataclasses import dataclass

from agents.decision import AgentDecision
from policy.policy import PolicyDecision


@dataclass(frozen=True)
class AgentExecutionResult:
    agent_decision: AgentDecision
    policy_decision: PolicyDecision