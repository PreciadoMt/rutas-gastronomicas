from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    duration = Column(String)  # e.g., "2 horas", "Medio día"
    cost = Column(Float)
    location = Column(String)
    city = Column(String, index=True)
    state = Column(String, default="Querétaro")
    image_url = Column(String, nullable=True)
    
    appointments = relationship("Appointment", back_populates="activity")