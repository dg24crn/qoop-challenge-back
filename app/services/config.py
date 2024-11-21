from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = 'postgresql://postgres:199596@localhost:5432/manage_db'

# Configuración para JWT
SECRET_KEY = "your-secret-key"  # Cambia esto por una clave secreta segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Tiempo de expiración del token en minutos

