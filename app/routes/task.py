from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.models.task import Task
from app.models.project import Project
from app.services.db import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = Task(
        name=task.name,
        project_id=task.project_id,
        assigned_to_id=task.assigned_to_id,
        completed=False,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

    if task_update.completed is not None:
        task.completed = task_update.completed
    if task_update.assigned_to_id is not None:
        task.assigned_to_id = task_update.assigned_to_id

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

    db.delete(task)
    db.commit()
    return {"message": f"Task with ID {task_id} deleted successfully"}


@router.get("/", response_model=list[TaskResponse])
def list_tasks(project_id: int = None, db: Session = Depends(get_db)):
    """
    List all tasks or filter tasks by project_id.
    """
    if project_id:
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
    else:
        tasks = db.query(Task).all()

    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_details(task_id: int, db: Session = Depends(get_db)):
    """
    Obtener detalles de una tarea específica por ID.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return task