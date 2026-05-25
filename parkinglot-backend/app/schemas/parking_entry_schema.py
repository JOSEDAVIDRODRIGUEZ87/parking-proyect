from pydantic import BaseModel

from typing import Optional

from datetime import datetime


# REQUEST CHECK-IN
class ParkingEntryRequest(BaseModel):

    vehicle_id: str


# RESPONSE
class ParkingEntryResponse(BaseModel):

    id: str

    vehicle_id: str

    entry_time: datetime

    exit_time: Optional[datetime] = None

    total_minutes: Optional[int] = None

    class Config:

        from_attributes = True