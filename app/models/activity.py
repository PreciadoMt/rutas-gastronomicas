from sqlalchemy import Column, Integer, String, Float, Boolean, Text
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
    activity_type = Column(String, default="Tour Gastronómico")  # NUEVO CAMPO
    is_active = Column(Boolean, default=True)  # NUEVO CAMPO - Para activar/desactivar sin eliminar
    
    appointments = relationship("Appointment", back_populates="activity")