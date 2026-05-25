from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.user_model import User
from app.schemas.auth_schema import LoginRequest
from app.utils.security import verify_password

router = APIRouter(prefix="/api/auth", tags=["Auth"])


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no existe")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {
        "message": "Login exitoso",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }