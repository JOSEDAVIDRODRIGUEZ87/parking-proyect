from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# 1. Importamos el Enum que creamos en el modelo de SQLAlchemy
from app.models.user_model import UserRole 


# REQUEST (Lo que el cliente envía)
class UserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    # 2. Agregamos el rol con un valor por defecto. 
    # Si el cliente no lo envía, automáticamente se creará como 'user'.
    role: UserRole = UserRole.USER


# RESPONSE (Lo que tu API devuelve)
class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str]
    is_active: bool
    # 3. Incluimos el rol en la respuesta para que el frontend sepa qué permisos tiene
    role: UserRole 
    created_at: datetime

    class Config:
        from_attributes = True