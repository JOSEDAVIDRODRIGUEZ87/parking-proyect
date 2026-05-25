import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.user_model import User, UserRole
from app.schemas.user_schema import UserRequest
from app.utils.security import hash_password

router = APIRouter(prefix="/api/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# LISTAR
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "email": u.email,
            "phone": u.phone,
            "role": u.role.value,
            "is_active": u.is_active
        }
        for u in users
    ]


# GET BY ID
@router.get("/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role.value,
        "is_active": user.is_active
    }


# CREATE
@router.post("/")
def create_user(request: UserRequest, db: Session = Depends(get_db)):

    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=409, detail="Email ya existe")

    user = User(
        id=str(uuid.uuid4()),
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone=request.phone,
        role=request.role if request.role else UserRole.USER,
        password_hash=hash_password(request.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Usuario creado",
        "data": {
            "id": user.id,
            "email": user.email,
            "role": user.role.value
        }
    }


# UPDATE
@router.put("/{user_id}")
def update_user(user_id: str, request: UserRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.first_name = request.first_name
    user.last_name = request.last_name
    user.email = request.email
    user.phone = request.phone

    if request.role:
        user.role = request.role

    if request.password:
        user.password_hash = hash_password(request.password)

    db.commit()
    db.refresh(user)

    return {"message": "Usuario actualizado"}


# DELETE
@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()

    return {"message": "Usuario eliminado"}