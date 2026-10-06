from agents.emergency_agent import EmergencyAgent
from decision.executor import DecisionExecutor
from decision.translator import DecisionTranslator


class AgentOrchestrator:
    def __init__(
        self,
        agent: EmergencyAgent,
        translator: DecisionTranslator,
        executor: DecisionExecutor,
    ) -> None:
        self._agent = agent
        self._translator = translator
        self._executor = executor

    def run(self) -> bool:
        decision = self._agent.observe_and_decide()

        if decision is None:
            return False

        action = self._translator.translate(decision)

        self._executor.execute(action)

        return True