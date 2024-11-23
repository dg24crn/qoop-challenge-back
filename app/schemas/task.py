from pydantic import BaseModel, Field
from typing import Optional


# Esquema para crear una tarea
class TaskCreate(BaseModel):
    name: str
    project_id: int
    assigned_to_id: Optional[int] = None


# Esquema para actualizar una tarea
class TaskUpdate(BaseModel):
    completed: Optional[bool] = Field(default=None, description="Estado de la tarea")
    assigned_to_id: Optional[int] = Field(default=None, description="ID del usuario asignado")


# Esquema de respuesta para las tareas
class TaskResponse(BaseModel):
    id: int
    name: str
    project_id: int
    assigned_to_id: Optional[int] = None
    completed: bool

    class Config:
        orm_mode = True