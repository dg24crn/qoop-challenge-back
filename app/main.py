import uvicorn
import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.db import Base, engine

# Importación de routers
from app.routes.user import router as user_router
from app.routes.project import router as project_router
from app.routes.task import router as task_router
from app.routes.auth import router as auth_router
from app.routes.team import router as team_router

# Ajustar el path del sistema
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Inicializar la aplicación FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir acceso desde cualquier origen para producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Manage API"}

# Registrar routers
app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(auth_router)
app.include_router(team_router)

# Punto de entrada para desarrollo local
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
