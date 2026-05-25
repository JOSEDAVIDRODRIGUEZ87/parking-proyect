from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.models.vehicle_model import Vehicle
from app.models.vehicle_model import VehicleType

from app.schemas.vehicle_schema import VehicleRequest

import uuid


router = APIRouter(
    prefix="/api/vehicles",
    tags=["Vehicles"]
)


# CONEXION DB
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# LISTAR TODOS LOS VEHICULOS
@router.get("/")
def get_vehicles(
    db: Session = Depends(get_db)
):

    vehicles = db.query(Vehicle).all()

    return vehicles


# OBTENER VEHICULO POR ID
@router.get("/{vehicle_id}")
def get_vehicle_by_id(
    vehicle_id: str,
    db: Session = Depends(get_db)
):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehiculo no encontrado"
        )

    return vehicle


# CREAR VEHICULO
@router.post("/")
def create_vehicle(
    request: VehicleRequest,
    db: Session = Depends(get_db)
):

    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.plate == request.plate
    ).first()

    if existing_vehicle:

        raise HTTPException(
            status_code=400,
            detail="La placa ya existe"
        )

    new_vehicle = Vehicle(
        id=str(uuid.uuid4()),
        plate=request.plate,
        brand=request.brand,
        model=request.model,
        color=request.color,
        vehicle_type=VehicleType(request.vehicle_type),
        user_id=request.user_id
    )

    db.add(new_vehicle)

    db.commit()

    db.refresh(new_vehicle)

    return {
        "message": "Vehiculo creado correctamente",
        "data": new_vehicle
    }


# ACTUALIZAR VEHICULO
@router.put("/{vehicle_id}")
def update_vehicle(
    vehicle_id: str,
    request: VehicleRequest,
    db: Session = Depends(get_db)
):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehiculo no encontrado"
        )

    vehicle.plate = request.plate
    vehicle.brand = request.brand
    vehicle.model = request.model
    vehicle.color = request.color
    vehicle.vehicle_type = VehicleType(request.vehicle_type)
    vehicle.user_id = request.user_id

    db.commit()

    db.refresh(vehicle)

    return {
        "message": "Vehiculo actualizado correctamente",
        "data": vehicle
    }


# ELIMINAR VEHICULO
@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db)
):

    vehicle = db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()

    if not vehicle:

        raise HTTPException(
            status_code=404,
            detail="Vehiculo no encontrado"
        )

    db.delete(vehicle)

    db.commit()

    return {
        "message": "Vehiculo eliminado correctamente"
    }