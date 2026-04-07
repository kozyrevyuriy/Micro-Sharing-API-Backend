from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.services import ride_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/rides/start")
def start_ride(user_id: int, vehicle_id: int, db: Session = Depends(get_db)):
    return ride_service.start_ride(db, user_id, vehicle_id)


@router.post("/rides/end")
def end_ride(user_id: int, db: Session = Depends(get_db)):
    return ride_service.end_ride(db, user_id)