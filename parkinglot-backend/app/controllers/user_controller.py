import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.user_model import User, UserRole  # <--- Importamos UserRole desde tu modelo
from app.schemas.user_schema import UserRequest

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

    # Nota: Asegúrate de que en tu UserRequest (pydantic) hayas agregado el campo role.
    # Si viene en el request, lo usamos; si no, dejamos que use el default asignando None 
    # o leyendo un default del esquema.
    new_user = User(
        id=str(uuid.uuid4()),
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone=request.phone,
        role=request.role if hasattr(request, 'role') else UserRole.USER  # <--- Asignamos el rol
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
    
    # <--- Permitimos actualizar el rol si viene en la petición
    if hasattr(request, 'role') and request.role is not None:
        user.role = request.role

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