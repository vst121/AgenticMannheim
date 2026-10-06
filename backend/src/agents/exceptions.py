from uuid import UUID


class AgentRunFailed(Exception):
    def __init__(
        self,
        run_id: UUID,
        cause: Exception,
    ) -> None:
        self.run_id = run_id
        self.cause = cause

        super().__init__(
            f"Agent run '{run_id}' failed: {cause}"
        )