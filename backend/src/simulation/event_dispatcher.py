from collections.abc import Callable
from domain.event import CityEvent


EventHandler = Callable[[CityEvent], None]


class EventDispatcher:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

    def subscribe(
        self,
        event_type: str,
        handler: EventHandler,
    ) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def dispatch(self, event: CityEvent) -> None:
        handlers = self._handlers.get(event.event_type.value, [])

        for handler in handlers:
            handler(event)
