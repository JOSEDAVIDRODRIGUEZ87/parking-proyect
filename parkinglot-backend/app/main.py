from fastapi import FastAPI

from app.config.database import engine
from app.config.database import Base

# MODELOS
from app.models.user_model import User
from app.models.vehicle_model import Vehicle
from app.models.parking_entry_model import ParkingEntry

# CONTROLLERS
from app.controllers.user_controller import router as user_router
from app.controllers.vehicle_controller import router as vehicle_router
from app.controllers.parking_entry_controller import router as parking_entry_router


app = FastAPI(
    title="Parking Lot API",
    description="API para gestion de parqueadero",
    version="1.0.0"
)


# CREAR TABLAS
Base.metadata.create_all(bind=engine)


# REGISTRAR ROUTERS
app.include_router(user_router)
app.include_router(vehicle_router)
app.include_router(parking_entry_router)


# ENDPOINT BASE
@app.get("/")
def home():

    return {
        "message": "Parking Lot API funcionando"
    }