from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    owner_id: int  # ID del usuario propietario

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True  # Esto permite que SQLAlchemy devuelva objetos compatibles con Pydantic
