import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from infrastructure.persistence.models.base import Base
from uuid import uuid4

from domain.road import Road, RoadType
from infrastructure.persistence.repositories.road_repository import RoadRepository


def test_add_and_get_road(db_session):
    start_intersection_id = uuid4()
    end_intersection_id = uuid4()

    road = Road(
        id=uuid4(),
        name="Example Street",
        road_type=RoadType.PRIMARY,
        start_intersection_id=start_intersection_id,
        end_intersection_id=end_intersection_id,
        length_meters=250.0,
        speed_limit_kmh=50.0,
        lanes=2,
    )

    repository = RoadRepository(db_session)

    repository.add(road)
    db_session.commit()

    result = repository.get(road.id)

    assert result is not None
    assert result.id == road.id
    assert result.name == road.name
    assert result.road_type == road.road_type
    assert result.length_meters == road.length_meters
    assert result.speed_limit_kmh == road.speed_limit_kmh
    assert result.lanes == road.lanes
    

@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
    engine.dispose()
