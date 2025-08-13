from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models import user, activity, appointment
from app.routers import users, activities, appointments
from app.middleware.cors import add_cors_middleware

# --- IMPORTA TODOS LOS ESQUEMAS CON REFERENCIAS ---
from app.schemas.appointment import AppointmentWithDetails
from app.schemas.user import UserWithAppointments
from app.schemas.activity import Activity  
from app.schemas.user import User

# Crear las tablas
user.Base.metadata.create_all(bind=engine)
activity.Base.metadata.create_all(bind=engine)
appointment.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rutas Gastronómicas Querétaro",
    description="API para gestión de rutas gastronómicas y reservas",
    version="1.0.0"
)

# Middleware
add_cors_middleware(app)

# Static files y templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(users.router)
app.include_router(activities.router)
app.include_router(appointments.router)

# --- RECONSTRUCCIÓN DE MODELOS ---
AppointmentWithDetails.model_rebuild()
UserWithAppointments.model_rebuild()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    all_activities = db.query(activity.Activity).limit(6).all()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "activities": all_activities}
    )

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/admin/activities", response_class=HTMLResponse)
def admin_activities(request: Request, db: Session = Depends(get_db)):
    activities = db.query(activity.Activity).all()
    return templates.TemplateResponse(
        "manage_activities.html", 
        {"request": request, "activities": activities}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)