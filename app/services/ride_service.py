from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.ride import Ride
from app.models.vehicle import Vehicle
from app.models.user import User


def start_ride(db: Session, user_id: int, vehicle_id: int):
    # проверка пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    # атомарное обновление vehicle
    updated = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id,
        Vehicle.status == "available"
    ).update({"status": "in_ride"})

    if updated == 0:
        raise HTTPException(status_code=400, detail="vehicle not available")

    # создаём поездку
    ride = Ride(
        user_id=user_id,
        vehicle_id=vehicle_id,
        start_time=datetime.utcnow(),
        status="active"
    )

    db.add(ride)
    db.commit()
    db.refresh(ride)

    return ride


def end_ride(db: Session, user_id: int):
    now = datetime.utcnow()

    # атомарное завершение ride
    updated = db.query(Ride).filter(
        Ride.user_id == user_id,
        Ride.status == "active"
    ).update({
        "status": "finished",
        "end_time": now
    })

    if updated == 0:
        raise HTTPException(status_code=400, detail="no active ride")

    # получаем ride
    ride = db.query(Ride).filter(
        Ride.user_id == user_id,
        Ride.end_time == now
    ).first()

    # освобождаем vehicle
    db.query(Vehicle).filter(
        Vehicle.id == ride.vehicle_id
    ).update({"status": "available"})

    # считаем цену
    duration = (ride.end_time - ride.start_time).seconds
    price = duration * 0.01

    db.commit()

    return {
        "ride_id": ride.id,
        "duration": duration,
        "price": price
    }