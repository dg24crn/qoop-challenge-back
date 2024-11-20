from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import user
from app.schemas import user as user_schemas
from app.auth import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta de registro de un nuevo usuario
@router.post("/register", response_model=user_schemas.User)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = db.query(user.User).filter(user.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear el nuevo usuario
    hashed_password = hash_password(user.password)  # Asegúrate de tener esta función de hashing
    db_user = user.User(email=user.email, username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
