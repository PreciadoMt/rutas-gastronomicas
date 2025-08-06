from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .appointment import AppointmentResponse

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

# ...existing code...

class UserWithAppointments(User):
    appointments: List['AppointmentResponse'] = []

    class Config:
        arbitrary_types_allowed = True

from app.schemas.appointment import AppointmentResponse  

# UserWithAppointments.model_rebuild()