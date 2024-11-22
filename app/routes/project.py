from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.project import ProjectCreate, ProjectResponse
from app.models.project import Project, ProjectMember
from app.models.user import User  # Importar User
from app.services.db import get_db
from app.models.task import Task
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    # Crear un nuevo proyecto
    new_project = Project(name=project.name, owner_id=project.owner_id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    List all projects owned by the authenticated user.
    """
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    return projects


@router.delete("/{project_id}", response_model=dict)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": f"Project with ID {project_id} deleted successfully"}


@router.post("/{project_id}/add_member", response_model=dict)
def add_member_to_project(project_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Add a member to a project by project_id and user_id.
    """
    # Verificar si el proyecto existe
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Verificar si el usuario existe
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Asociar el miembro al proyecto
    project_member = ProjectMember(project_id=project_id, user_id=user_id)
    db.add(project_member)
    db.commit()
    db.refresh(project_member)

    return {"message": f"User {user_id} added to project {project_id} successfully"}


@router.get("/{project_id}/members", response_model=list[dict])
def list_project_members(project_id: int, db: Session = Depends(get_db)):
    """
    List all members of a specific project.
    """
    # Verificar si el proyecto existe
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Obtener los miembros del proyecto
    members = (
        db.query(ProjectMember, User)
        .join(User, ProjectMember.user_id == User.id)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )

    # Formatear los datos para la respuesta
    response = [
        {
            "user_id": member.User.id,
            "first_name": member.User.first_name,
            "last_name": member.User.last_name,
            "email": member.User.email,
        }
        for member in members
    ]

    return response


@router.delete("/{project_id}/remove_member/{user_id}", response_model=dict)
def remove_member_from_project(
    project_id: int, user_id: int, db: Session = Depends(get_db)
):
    """
    Eliminar un miembro de un proyecto por project_id y user_id.
    """
    # Verificar si el proyecto existe
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Verificar si el miembro está asociado al proyecto
    project_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id, ProjectMember.user_id == user_id
        )
        .first()
    )
    if not project_member:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} is not a member of project {project_id}",
        )

    # Eliminar al miembro del proyecto
    db.delete(project_member)
    db.commit()

    return {"message": f"User {user_id} removed from project {project_id} successfully"}


@router.get("/{project_id}/progress", response_model=dict)
def get_project_progress(project_id: int, db: Session = Depends(get_db)):
    """
    Calcula el porcentaje de progreso de un proyecto basado en las tareas completadas.
    """
    # Verificar si el proyecto existe
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Obtener todas las tareas del proyecto
    tasks = db.query(Task).filter(Task.project_id == project_id).all()

    # Calcular el progreso
    if not tasks:  # Si no hay tareas
        progress = 0
    else:
        completed_tasks = sum(task.completed for task in tasks)  # Tareas completadas
        total_tasks = len(tasks)  # Total de tareas
        progress = (completed_tasks / total_tasks) * 100

    # Retornar el progreso
    return {"project_id": project_id, "progress": f"{progress:.2f}%"}


@router.get("/team/{team_id}", response_model=list[ProjectResponse])
def get_team_projects(team_id: int, db: Session = Depends(get_db)):
    """
    Obtener todos los proyectos asociados al equipo.
    """
    # Verificar si el equipo existe
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found.")

    # Obtener proyectos del propietario del equipo
    owner_projects = db.query(Project).filter(Project.owner_id == team.owner_id).all()

    return owner_projects
