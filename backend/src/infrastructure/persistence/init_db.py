from .database import engine
from .models import Base
from .models import CityModel  # noqa: F401


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")    