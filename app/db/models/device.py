from dataclasses import dataclass
from app.db.models.location import Location


@dataclass
class Device:
    id: str
    brand: str
    model: str
    os: str
    location: Location