from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Index
from datetime import datetime
from app.db import Base

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    status = Column(String, default="active")

    Index("ix_user_active_ride", "user_id", "status")