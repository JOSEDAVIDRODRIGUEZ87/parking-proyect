from pydantic import BaseModel
from pydantic import Field

from typing import Optional

from enum import Enum


class VehicleType(str, Enum):

    CAR = "CAR"
    MOTORCYCLE = "MOTORCYCLE"


# REQUEST
class VehicleRequest(BaseModel):

    plate: str = Field(
        min_length=5,
        max_length=10
    )

    brand: str = Field(
        min_length=2,
        max_length=100
    )

    model: str = Field(
        min_length=1,
        max_length=100
    )

    color: str = Field(
        min_length=2,
        max_length=50
    )

    vehicle_type: VehicleType

    user_id: str


# RESPONSE
class VehicleResponse(BaseModel):

    id: str

    plate: str

    brand: str

    model: str

    color: str

    vehicle_type: VehicleType

    user_id: str

    class Config:

        from_attributes = True