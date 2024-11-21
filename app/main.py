import sys
import os

from app.routes.user import router as user_router
from app.routes.project import router as project_router
from app.routes.task import router as task_router
from app.routes.auth import router as auth_router

# Agregar la carpeta raíz del proyecto al sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from app.services.db import Base, engine
from app.models import user, project, task

app = FastAPI()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to Manage API"}

app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(auth_router)