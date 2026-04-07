from pydantic import BaseModel

class VehicleCreate(BaseModel):
    status: str = "available"