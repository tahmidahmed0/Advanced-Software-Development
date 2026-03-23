from dataclasses import dataclass

@dataclass
class Apartment:
    apartment_id: int | None
    city: str
    address: str
    apartment_type: str
    rooms: int
    monthly_rent: float
    occupancy_status: str = "Vacant"
