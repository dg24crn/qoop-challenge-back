import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.db import Base, engine

from app.routes.user import router as user_router
from app.routes.project import router as project_router
from app.routes.task import router as task_router
from app.routes.auth import router as auth_router
from app.routes.team import router as team_router

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Origen del frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

#! Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Welcome to Manage API"}


app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(auth_router)
app.include_router(team_router)
