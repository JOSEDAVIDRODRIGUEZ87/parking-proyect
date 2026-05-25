from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.user_model import User
from app.schemas.user_schema import UserRequest

import uuid


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


# CONEXION DB
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# LISTAR TODOS LOS USUARIOS
@router.get("/")
def get_users(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users


# OBTENER USUARIO POR ID
@router.get("/{user_id}")
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


# CREAR USUARIO
@router.post("/")
def create_user(
    request: UserRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="El correo ya existe"
        )

    new_user = User(
        id=str(uuid.uuid4()),
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone=request.phone
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "Usuario creado correctamente",
        "data": new_user
    }


# ACTUALIZAR USUARIO
@router.put("/{user_id}")
def update_user(
    user_id: str,
    request: UserRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    user.first_name = request.first_name
    user.last_name = request.last_name
    user.email = request.email
    user.phone = request.phone

    db.commit()

    db.refresh(user)

    return {
        "message": "Usuario actualizado correctamente",
        "data": user
    }


# ELIMINAR USUARIO
@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(user)

    db.commit()

    return {
        "message": "Usuario eliminado correctamente"
    }