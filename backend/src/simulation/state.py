from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class SimulationState:
    current_time: datetime
    tick: int = 0

    @classmethod
    def create(cls) -> "SimulationState":
        return cls(
            current_time=datetime.now(timezone.utc),
            tick=0,
        )

    def advance(self, seconds: float) -> None:
        from datetime import timedelta

        self.current_time += timedelta(seconds=seconds)
        self.tick += 1