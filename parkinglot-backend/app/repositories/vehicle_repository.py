from sqlalchemy.orm import Session

from app.models.vehicle_model import Vehicle


class VehicleRepository:


    # LISTAR TODOS
    @staticmethod
    def get_all(db: Session):

        return db.query(Vehicle).all()


    # BUSCAR POR ID
    @staticmethod
    def get_by_id(
        db: Session,
        vehicle_id: str
    ):

        return db.query(Vehicle).filter(
            Vehicle.id == vehicle_id
        ).first()


    # BUSCAR POR PLACA
    @staticmethod
    def get_by_plate(
        db: Session,
        plate: str
    ):

        return db.query(Vehicle).filter(
            Vehicle.plate == plate
        ).first()


    # LISTAR VEHICULOS POR USUARIO
    @staticmethod
    def get_by_user_id(
        db: Session,
        user_id: str
    ):

        return db.query(Vehicle).filter(
            Vehicle.user_id == user_id
        ).all()


    # CREAR VEHICULO
    @staticmethod
    def create(
        db: Session,
        vehicle: Vehicle
    ):

        db.add(vehicle)

        db.commit()

        db.refresh(vehicle)

        return vehicle


    # ACTUALIZAR VEHICULO
    @staticmethod
    def update(
        db: Session,
        vehicle: Vehicle
    ):

        db.commit()

        db.refresh(vehicle)

        return vehicle


    # ELIMINAR VEHICULO
    @staticmethod
    def delete(
        db: Session,
        vehicle: Vehicle
    ):

        db.delete(vehicle)

        db.commit()

        return True