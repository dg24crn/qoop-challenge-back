from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from app.models.user import User
from app.services.db import get_db
from app.services.auth import verify_password, create_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Endpoint para registrar un usuario
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Crear nuevo usuario con contraseña hasheada
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=User.hash_password(user.password),  # Hasheamos la contraseña
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Endpoint para listar todos los usuarios
@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """
    List all registered users.
    """
    users = db.query(User).all()
    return users

# Endpoint para login de usuarios
@router.post("/login", response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and generate JWT token.
    """
    # Buscar usuario por email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar token JWT
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
