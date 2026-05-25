from pydantic import BaseModel
from pydantic import EmailStr


class UserRequest(BaseModel):

    name: str
    email: EmailStr


class UserResponse(BaseModel):

    id: str
    name: str
    email: EmailStr

    class Config:

        from_attributes = True