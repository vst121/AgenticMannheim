from agents.run import AgentRun


class AgentRunFailed(Exception):
    def __init__(
        self,
        run: AgentRun,
        cause: Exception,
    ) -> None:
        self.run = run
        self.cause = cause

        super().__init__(
            f"Agent run '{run.id}' failed: {cause}"
        )