from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from app.models.appointment import AppointmentStatus

class AppointmentBase(BaseModel):
    activity_id: int
    appointment_date: datetime
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    user_id: int
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

if TYPE_CHECKING:
    from app.schemas.activity import Activity
    from app.schemas.user import User

class AppointmentWithDetails(AppointmentResponse):
    activity: 'Activity'
    user: 'User'

# AppointmentWithDetails.model_rebuild()