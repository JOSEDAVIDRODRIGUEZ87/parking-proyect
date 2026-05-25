import uuid
from sqlalchemy import Column, String, Boolean, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.config.database import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)

    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

    is_active = Column(Boolean, default=True)

    # 🔐 PASSWORD
    password_hash = Column(String(255), nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    
    vehicles = relationship("Vehicle", back_populates="user")