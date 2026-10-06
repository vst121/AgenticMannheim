from uuid import uuid4

from sqlalchemy import select

from domain.intersection import TrafficLightState
from domain.road import RoadType
from infrastructure.persistence.database import SessionLocal
from infrastructure.persistence.models.city import CityModel
from infrastructure.persistence.models.intersection import IntersectionModel
from infrastructure.persistence.models.road import RoadModel


def seed_database() -> None:
    with SessionLocal() as session:
        existing_city = session.scalar(
            select(CityModel).where(
                CityModel.name == "Mannheim",
                CityModel.area == "Innenstadt",
            )
        )

        if existing_city is not None:
            print("Mannheim Innenstadt already exists. Nothing to seed.")
            return

        city = CityModel(
            name="Mannheim",
            area="Innenstadt",
            latitude=49.4875,
            longitude=8.4660,
        )

        intersection_a = IntersectionModel(
            id=uuid4(),
            name="Mannheim Innenstadt A",
            latitude=49.4875,
            longitude=8.4660,
            traffic_light=TrafficLightState.RED.value,
        )

        intersection_b = IntersectionModel(
            id=uuid4(),
            name="Mannheim Innenstadt B",
            latitude=49.4880,
            longitude=8.4670,
            traffic_light=TrafficLightState.RED.value,
        )

        road = RoadModel(
            id=uuid4(),
            name="Example Road",
            road_type=RoadType.PRIMARY.value,
            start_intersection_id=intersection_a.id,
            end_intersection_id=intersection_b.id,
            length_meters=250.0,
            speed_limit_kmh=50.0,
            lanes=2,
        )

        session.add_all(
            [
                city,
                intersection_a,
                intersection_b,
                road,
            ]
        )

        session.commit()

        print("Seeded Mannheim Innenstadt.")


if __name__ == "__main__":
    seed_database()