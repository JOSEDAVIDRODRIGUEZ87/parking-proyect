from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from datetime import datetime
import uuid

from fastapi_mail import MessageSchema

from app.config.database import SessionLocal
from app.config.mail_config import fast_mail

from app.models.vehicle_model import Vehicle
from app.models.parking_entry_model import ParkingEntry

from app.schemas.parking_entry_schema import ParkingEntryRequest


router = APIRouter(
    prefix="/api/parking-entries",
    tags=["Parking Entries"]
)


# =========================
# DB CONNECTION
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# LISTAR TODOS
# =========================
@router.get("/")
def get_parking_entries(db: Session = Depends(get_db)):
    return db.query(ParkingEntry).all()


# =========================
# OBTENER POR ID
# =========================
@router.get("/{parking_entry_id}")
def get_parking_entry_by_id(parking_entry_id: str, db: Session = Depends(get_db)):

    entry = db.query(ParkingEntry).filter(
        ParkingEntry.id == parking_entry_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return entry


# =========================
# CHECK-IN
# =========================
@router.post("/check-in")
def check_in(request: ParkingEntryRequest, db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == request.vehicle_id
    ).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehiculo no encontrado")

    # validar ingreso activo
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
        notes=request.notes  # 🆕 NOTA
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return {
        "message": "Ingreso registrado correctamente",
        "data": new_entry
    }


# =========================
# CHECK-OUT + EMAIL
# =========================
@router.put("/check-out/{parking_entry_id}")
async def check_out(parking_entry_id: str, db: Session = Depends(get_db)):

    entry = db.query(ParkingEntry).filter(
        ParkingEntry.id == parking_entry_id
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    if entry.exit_time is not None:
        raise HTTPException(status_code=409, detail="La salida ya fue registrada")

    # =========================
    # CÁLCULOS
    # =========================
    exit_time = datetime.now()

    total_minutes = int(
        (exit_time - entry.entry_time).total_seconds() / 60
    )

    rate_per_minute = 50
    total_amount = total_minutes * rate_per_minute

    entry.exit_time = exit_time
    entry.total_minutes = total_minutes
    entry.rate_per_minute = rate_per_minute
    entry.total_amount = total_amount

    db.commit()
    db.refresh(entry)

    # =========================
    # EMAIL DESTINATARIO
    # =========================
    email_to = None

    if entry.vehicle and entry.vehicle.user:
        email_to = entry.vehicle.user.email

    # =========================
    # EMAIL TEMPLATE
    # =========================
    if email_to:

        html = f"""
        <h2>🚗 Ticket de Parqueadero</h2>
        <p><b>Placa:</b> {entry.vehicle.plate}</p>
        <p><b>Tiempo total:</b> {total_minutes} minutos</p>
        <p><b>Total a pagar:</b> ${total_amount}</p>
        <p><b>Hora salida:</b> {exit_time}</p>
        """

        message = MessageSchema(
            subject="Factura Parqueadero - Salida Vehículo",
            recipients=[email_to],
            body=html,
            subtype="html"
        )

        await fast_mail.send_message(message)

    return {
        "message": "Salida registrada correctamente",
        "time_total_minutes": total_minutes,
        "rate_per_minute": rate_per_minute,
        "total_amount": total_amount,
        "email_sent": bool(email_to),
        "data": entry
    }