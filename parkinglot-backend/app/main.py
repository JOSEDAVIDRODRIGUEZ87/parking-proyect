from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import engine, Base

# =========================
# MODELOS (IMPORTACIÓN OBLIGATORIA PARA CREATE_ALL)
# =========================
from app.models.user_model import User
from app.models.vehicle_model import Vehicle
from app.models.parking_entry_model import ParkingEntry

# =========================
# CONTROLLERS
# =========================
from app.controllers.user_controller import router as user_router
from app.controllers.vehicle_controller import router as vehicle_router
from app.controllers.parking_entry_controller import router as parking_entry_router
from app.controllers.auth_controller import router as auth_router


# =========================
# APP
# =========================
app = FastAPI(
    title="Parking Lot API",
    description="API para gestión de parqueadero",
    version="1.0.0"
)


# =========================
# CORS (ANGULAR)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# CREAR TABLAS (SQLALCHEMY)
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# ROUTERS
# =========================
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(vehicle_router)
app.include_router(parking_entry_router)


# =========================
# ENDPOINTS BASE
# =========================
@app.get("/")
def home():
    return {
        "message": "Parking Lot API funcionando 🚗"
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "parking-lot-api"
    }