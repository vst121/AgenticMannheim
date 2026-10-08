from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from uuid import UUID


@dataclass
class SimulationState:
    current_time: datetime
    tick: int = 0
    emergency_light_started_at: dict[UUID, float] = field(
        default_factory=dict,
    )

    @classmethod
    def create(cls) -> "SimulationState":
        return cls(
            current_time=datetime.now(timezone.utc),
            tick=0,
        )

    def advance(self, seconds: float) -> None:
        self.current_time += timedelta(seconds=seconds)
        self.tick += 1

    def start_emergency_light(
        self,
        intersection_id: UUID,
    ) -> None:
        self.emergency_light_started_at[intersection_id] = (
            self.current_time.timestamp()
        )

    def get_emergency_light_start(
        self,
        intersection_id: UUID,
    ) -> float | None:
        return self.emergency_light_started_at.get(
            intersection_id
        )

    def clear_emergency_light(
        self,
        intersection_id: UUID,
    ) -> None:
        self.emergency_light_started_at.pop(
            intersection_id,
            None,
        )
