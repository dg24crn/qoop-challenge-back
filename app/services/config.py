from dotenv import load_dotenv
import os

# Cargar las variables desde el archivo .env
load_dotenv()

# Configuración de base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("La variable DATABASE_URL no está configurada en el archivo .env")

# Configuración para JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # Valor predeterminado si falta en .env
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
