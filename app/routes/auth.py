from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.services.db import get_db
from app.services.auth import verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Endpoint para iniciar sesión. Recibe credenciales y genera un token de acceso JWT.
    """
    # Buscar al usuario por email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Verificar la contraseña
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Crear un token de acceso
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
