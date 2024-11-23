from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.services.config import DATABASE_URL

# Crear el motor de conexión usando DATABASE_URL
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"} if "localhost" not in DATABASE_URL else {})

# Configurar la sesión y el modelo base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
