from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from datetime import datetime

import uuid

from app.config.database import SessionLocal

from app.models.vehicle_model import Vehicle
from app.models.parking_entry_model import ParkingEntry

from app.schemas.parking_entry_schema import ParkingEntryRequest


router = APIRouter(
    prefix="/api/parking-entries",
    tags=["Parking Entries"]
)


# CONEXION DB
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# LISTAR TODOS LOS INGRESOS
@router.get("/")
def get_parking_entries(
    db: Session = Depends(get_db)
):

    parking_entries = db.query(ParkingEntry).all()

    return parking_entries


# OBTENER INGRESO POR ID
@router.get("/{parking_entry_id}")
def get_parking_entry_by_id(
    parking_entry_id: str,
    db: Session = Depends(get_db)
):

    parking_entry = db.query(ParkingEntry).filter(
        ParkingEntry.id == parking_entry_id
    ).first()

    if not parking_entry:

        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    return parking_entry


# REGISTRAR INGRESO VEHICULO
@router.post("/check-in")
def check_in(request: ParkingEntryRequest, db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == request.vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

    active_entry = db.query(ParkingEntry).filter(
        ParkingEntry.vehicle_id == request.vehicle_id,
        ParkingEntry.exit_time == None
    ).first()

    if active_entry:
        raise HTTPException(
            status_code=409,
            detail="El vehiculo ya se encuentra dentro del parqueadero"
        )

    new_entry = ParkingEntry(
        id=str(uuid.uuid4()),
        vehicle_id=request.vehicle_id,
        notes=request.notes  # ✅ AQUÍ YA FUNCIONA
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "message": "Ingreso registrado correctamente",
        "data": new_entry
    }

# REGISTRAR SALIDA VEHICULO
@router.put("/check-out/{parking_entry_id}")
def check_out(
    parking_entry_id: str,
    db: Session = Depends(get_db)
):

    parking_entry = db.query(ParkingEntry).filter(
        ParkingEntry.id == parking_entry_id
    ).first()

    if not parking_entry:

        raise HTTPException(
            status_code=404,
            detail="Registro no encontrado"
        )

    if parking_entry.exit_time is not None:

        raise HTTPException(
            status_code=409,
            detail="La salida ya fue registrada"
        )

    exit_time = datetime.now()

    total_minutes = int(
        (exit_time - parking_entry.entry_time).total_seconds() / 60
    )

    # TARIFA FIJA
    rate_per_minute = 50

    # TOTAL A PAGAR
    total_amount = total_minutes * rate_per_minute

    parking_entry.exit_time = exit_time
    parking_entry.total_minutes = total_minutes
    parking_entry.rate_per_minute = rate_per_minute
    parking_entry.total_amount = total_amount

    db.commit()

    db.refresh(parking_entry)

    return {
        "message": "Salida registrada correctamente",
        "time_total_minutes": total_minutes,
        "rate_per_minute": rate_per_minute,
        "total_amount": total_amount,
        "data": parking_entry
    }