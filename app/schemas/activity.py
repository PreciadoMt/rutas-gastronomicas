from pydantic import BaseModel
from typing import Optional

class ActivityBase(BaseModel):
    name: str
    description: str
    duration: str
    cost: float
    location: str
    city: str
    state: str = "Querétaro"
    image_url: Optional[str] = None
    activity_type: str = "Tour Gastronómico"

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    cost: Optional[float] = None
    location: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    image_url: Optional[str] = None
    activity_type: Optional[str] = None

class Activity(ActivityBase):
    id: int
    is_active: bool = True
    
    class Config:
        from_attributes = True