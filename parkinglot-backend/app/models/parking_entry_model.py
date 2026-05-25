from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.config.database import Base

import uuid


class ParkingEntry(Base):

    __tablename__ = "parking_entries"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    vehicle_id = Column(
        String(36),
        ForeignKey("vehicles.id"),
        nullable=False
    )

    entry_time = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    exit_time = Column(
        TIMESTAMP,
        nullable=True
    )

    total_minutes = Column(
        Integer,
        nullable=True
    )

    vehicle = relationship(
        "Vehicle"
    )