from pydantic import BaseModel
from pydantic import EmailStr

from typing import Optional

from datetime import datetime


# REQUEST
class UserRequest(BaseModel):

    first_name: str

    last_name: str

    email: EmailStr

    phone: Optional[str] = None


# RESPONSE
class UserResponse(BaseModel):

    id: str

    first_name: str

    last_name: str

    email: EmailStr

    phone: Optional[str]

    is_active: bool

    created_at: datetime

    class Config:

        from_attributes = True