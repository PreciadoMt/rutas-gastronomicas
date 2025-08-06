from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models.appointment import Appointment, AppointmentStatus
from app.schemas.appointment import (
    AppointmentCreate, 
    AppointmentUpdate, 
    AppointmentResponse,
    AppointmentWithDetails
)

router = APIRouter(prefix="/appointments", tags=["appointments"])
templates = Jinja2Templates(directory="app/templates")

@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate, 
    user_id: int,
    db: Session = Depends(get_db)
):
    db_appointment = Appointment(
        user_id=user_id,
        **appointment.dict()
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.get("/", response_model=List[AppointmentWithDetails])
def read_appointments(
    skip: int = 0, 
    limit: int = 100,
    user_id: Optional[int] = None,
    activity_id: Optional[int] = None,
    status: Optional[AppointmentStatus] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Appointment)
    
    if user_id:
        query = query.filter(Appointment.user_id == user_id)
    if activity_id:
        query = query.filter(Appointment.activity_id == activity_id)
    if status:
        query = query.filter(Appointment.status == status)
    
    appointments = query.offset(skip).limit(limit).all()
    return appointments

@router.get("/{appointment_id}", response_model=AppointmentWithDetails)
def read_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db)
):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    update_data = appointment_update.dict(exclude_unset=True)
    if update_data:
        update_data['updated_at'] = datetime.utcnow()
        for key, value in update_data.items():
            setattr(db_appointment, key, value)
        
        db.commit()
        db.refresh(db_appointment)
    
    return db_appointment

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db.delete(db_appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}

@router.get("/user/{user_id}/history", response_model=List[AppointmentWithDetails])
def get_user_appointment_history(user_id: int, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.user_id == user_id).all()
    return appointments

# Ruta HTML
@router.get("/view/calendar", response_class=HTMLResponse)
def appointments_page(request: Request, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return templates.TemplateResponse(
        "appointments.html", 
        {"request": request, "appointments": appointments}
    )