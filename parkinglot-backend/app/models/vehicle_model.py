from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import Enum

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.config.database import Base

import enum
import uuid


class VehicleType(str, enum.Enum):

    CAR = "CAR"
    MOTORCYCLE = "MOTORCYCLE"


class Vehicle(Base):

    __tablename__ = "vehicles"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    plate = Column(
        String(10),
        unique=True,
        nullable=False
    )

    brand = Column(
        String(100),
        nullable=False
    )

    model = Column(
        String(100),
        nullable=False
    )

    color = Column(
        String(50),
        nullable=False
    )

    vehicle_type = Column(
        Enum(VehicleType),
        nullable=False
    )

    user_id = Column(
        String(36),
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="vehicles"
    )