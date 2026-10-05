from domain.event import CityEvent, CityEventType

from ..models.event import EventModel


def to_domain(model: EventModel) -> CityEvent:
    return CityEvent(
        id=model.id,
        event_type=CityEventType(model.event_type),
        timestamp=model.timestamp,
        aggregate_id=model.aggregate_id,
        payload=model.payload,
    )


def to_model(event: CityEvent) -> EventModel:
    return EventModel(
        id=event.id,
        event_type=event.event_type.value,
        timestamp=event.timestamp,
        aggregate_id=event.aggregate_id,
        payload=event.payload,
    )