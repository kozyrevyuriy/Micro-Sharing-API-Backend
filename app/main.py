from fastapi import FastAPI
from app.db import engine, Base
from app.models.user import User
from app.routers import user
from app.models.vehicle import Vehicle
from app.routers import vehicle
from app.models.ride import Ride
from app.routers import ride

app = FastAPI()


@app.get("/ping")
def read_root():
    return {"ok"}

Base.metadata.create_all(bind=engine)
app.include_router(user.router)
app.include_router(vehicle.router)
app.include_router(ride.router)