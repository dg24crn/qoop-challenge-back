from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.user import User as UserSchema
import jwt
from datetime import datetime, timedelta

# Configuración del esquema de autenticación (token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "secret_key"  # Cambia esto por una clave secreta más segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Función para verificar el token y obtener el usuario actual
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    return user

# Dependencia para extraer el usuario actual
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return verify_token(token, db)
