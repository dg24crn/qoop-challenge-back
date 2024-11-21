from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from app.models.user import User
from app.services.db import get_db
from app.services.auth import verify_password, create_access_token
from app.services.dependencies import get_current_user  # Importar la dependencia para obtener el usuario actual

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

# Endpoint para obtener el usuario actual
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Devuelve los datos del usuario autenticado basado en el token.
    """
    print(f"Usuario autenticado: {current_user.email}")  # Depuración
    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "is_subscribed": current_user.is_subscribed,
    }

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
    print(f"Token generado para {user.email}: {access_token}")  # Depuración
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint para activar suscripción
@router.post("/{user_id}/subscribe", response_model=dict)
def subscribe_user(user_id: int, db: Session = Depends(get_db)):
    """
    Activar suscripción para un usuario.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_subscribed = True
    db.commit()
    return {"message": f"Subscription activated for user {user_id}"}

# Endpoint para cancelar suscripción
@router.post("/{user_id}/unsubscribe", response_model=dict)
def unsubscribe_user(user_id: int, db: Session = Depends(get_db)):
    """
    Cancelar suscripción para un usuario.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_subscribed = False
    db.commit()
    return {"message": f"Subscription cancelled for user {user_id}"}

# Endpoint para verificar estado de suscripción
@router.get("/{user_id}/subscription-status", response_model=dict)
def check_subscription_status(user_id: int, db: Session = Depends(get_db)):
    """
    Verificar si un usuario tiene una suscripción activa.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"user_id": user.id, "is_subscribed": user.is_subscribed}
