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

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    
    class Config:
        from_attributes = True