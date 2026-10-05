from fastapi import APIRouter

from digital_twin.twin import DigitalTwin

router = APIRouter(prefix="/api/city", tags=["City"])

digital_twin = DigitalTwin()


@router.get("/state")
async def get_city_state():
    state = digital_twin.get_state()

    return {
        "city": {
            "name": state.city.name,
            "area": state.city.area,
            "latitude": state.city.latitude,
            "longitude": state.city.longitude,
        },
        "vehicles": [],
        "intersections": [],
    }