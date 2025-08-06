from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, Activity as ActivitySchema

router = APIRouter(prefix="/activities", tags=["activities"])
templates = Jinja2Templates(directory="app/templates")

@router.post("/", response_model=ActivitySchema)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.get("/", response_model=List[ActivitySchema])
def read_activities(
    skip: int = 0, 
    limit: int = 100, 
    city: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Activity)
    if city:
        query = query.filter(Activity.city.ilike(f"%{city}%"))
    activities = query.offset(skip).limit(limit).all()
    return activities

@router.get("/{activity_id}", response_model=ActivitySchema)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.put("/{activity_id}", response_model=ActivitySchema)
def update_activity(
    activity_id: int, 
    activity: ActivityCreate, 
    db: Session = Depends(get_db)
):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    for key, value in activity.dict().items():
        setattr(db_activity, key, value)
    
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db.delete(db_activity)
    db.commit()
    return {"message": "Activity deleted successfully"}

# Ruta HTML
@router.get("/view/all", response_class=HTMLResponse)
def activities_page(request: Request, db: Session = Depends(get_db)):
    activities = db.query(Activity).all()
    return templates.TemplateResponse(
        "activities.html", 
        {"request": request, "activities": activities}
    )