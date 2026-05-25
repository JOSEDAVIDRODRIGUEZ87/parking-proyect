from sqlalchemy.orm import Session

from app.models.user_model import User


class UserRepository:


    # LISTAR TODOS
    @staticmethod
    def get_all(db: Session):

        return db.query(User).all()


    # BUSCAR POR ID
    @staticmethod
    def get_by_id(
        db: Session,
        user_id: str
    ):

        return db.query(User).filter(
            User.id == user_id
        ).first()


    # BUSCAR POR EMAIL
    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):

        return db.query(User).filter(
            User.email == email
        ).first()


    # CREAR USUARIO
    @staticmethod
    def create(
        db: Session,
        user: User
    ):

        db.add(user)

        db.commit()

        db.refresh(user)

        return user


    # ACTUALIZAR USUARIO
    @staticmethod
    def update(
        db: Session,
        user: User
    ):

        db.commit()

        db.refresh(user)

        return user


    # ELIMINAR USUARIO
    @staticmethod
    def delete(
        db: Session,
        user: User
    ):

        db.delete(user)

        db.commit()

        return True