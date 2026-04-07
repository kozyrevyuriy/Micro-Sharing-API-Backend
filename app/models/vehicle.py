from sqlalchemy import Column, Integer, Enum
import enum
from app.db import Base


class VehicleStatus(str, enum.Enum):
    available = "available"
    in_ride = "in_ride"
    broken = "broken"
    unavailable = "unavailable"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(VehicleStatus), default=VehicleStatus.available)