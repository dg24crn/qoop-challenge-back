from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.services.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Contexto de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear una contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear un token JWT
def create_access_token(data: dict) -> str:
    """
    Genera un token JWT con un tiempo de expiración.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar y decodificar un token JWT
def verify_access_token(token: str) -> dict:
    """
    Decodifica el token JWT y verifica su validez.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
