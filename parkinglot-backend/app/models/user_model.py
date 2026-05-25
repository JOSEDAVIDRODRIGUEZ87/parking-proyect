import uuid
from enum import Enum as PyEnum # Importamos el Enum de Python

from app.config.database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Enum, String  # Añadimos Enum de SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


# 1. Definimos los roles permitidos
class UserRole(str, PyEnum):
    ADMIN = "admin"
    USER = "user"
    MECHANIC = "mechanic"  # (Ejemplo por si tu app es de vehículos)


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    first_name = Column(
        String(100),
        nullable=False
    )

    last_name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=True
    )

    # 2. Agregamos el campo rol con un valor por defecto
    role = Column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )

    vehicles = relationship(
        "Vehicle",
        back_populates="user",
        cascade="all, delete"
    )