from sqlalchemy import select

from infrastructure.persistence.database import SessionLocal
from infrastructure.persistence.models.city import CityModel


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

        session.add(city)
        session.commit()

        print("Seeded Mannheim Innenstadt.")


if __name__ == "__main__":
    seed_database()