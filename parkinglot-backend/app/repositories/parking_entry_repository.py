from sqlalchemy.orm import Session

from app.models.parking_entry_model import ParkingEntry


class ParkingEntryRepository:


    # LISTAR TODOS LOS REGISTROS
    @staticmethod
    def get_all(db: Session):

        return db.query(ParkingEntry).all()


    # BUSCAR POR ID
    @staticmethod
    def get_by_id(
        db: Session,
        parking_entry_id: str
    ):

        return db.query(ParkingEntry).filter(
            ParkingEntry.id == parking_entry_id
        ).first()


    # BUSCAR INGRESO ACTIVO POR VEHICULO
    @staticmethod
    def get_active_by_vehicle_id(
        db: Session,
        vehicle_id: str
    ):

        return db.query(ParkingEntry).filter(
            ParkingEntry.vehicle_id == vehicle_id,
            ParkingEntry.exit_time == None
        ).first()


    # LISTAR VEHICULOS ACTIVOS
    @staticmethod
    def get_active_entries(db: Session):

        return db.query(ParkingEntry).filter(
            ParkingEntry.exit_time == None
        ).all()


    # CREAR REGISTRO
    @staticmethod
    def create(
        db: Session,
        parking_entry: ParkingEntry
    ):

        db.add(parking_entry)

        db.commit()

        db.refresh(parking_entry)

        return parking_entry


    # ACTUALIZAR REGISTRO
    @staticmethod
    def update(
        db: Session,
        parking_entry: ParkingEntry
    ):

        db.commit()

        db.refresh(parking_entry)

        return parking_entry


    # ELIMINAR REGISTRO
    @staticmethod
    def delete(
        db: Session,
        parking_entry: ParkingEntry
    ):

        db.delete(parking_entry)

        db.commit()

        return True