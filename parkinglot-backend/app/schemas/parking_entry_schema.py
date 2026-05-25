from pydantic import BaseModel

from typing import Optional

from datetime import datetime

from decimal import Decimal


# REQUEST CHECK-IN
class ParkingEntryRequest(BaseModel):
    vehicle_id: str
    notes: Optional[str] = None

# RESPONSE
class ParkingEntryResponse(BaseModel):

    id: str

    vehicle_id: str

    entry_time: datetime

    exit_time: Optional[datetime] = None

    total_minutes: Optional[int] = None

    rate_per_minute: Optional[Decimal] = None

    total_amount: Optional[Decimal] = None

    class Config:

        from_attributes = True