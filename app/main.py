from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import project, auth  # Importa las rutas de auth

app = FastAPI()

app.include_router(project.router)  # Añade las rutas de proyectos
app.include_router(auth.router)  # Añade las rutas de autenticación

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get('/')
def welcome_message():
    return "Welcome to our pageee!"
