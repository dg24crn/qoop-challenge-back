from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.project import Project
from app.models.user import User
from app.schemas import project as project_schemas
from app.auth import get_current_user 

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear un nuevo proyecto
@router.post("/", response_model=project_schemas.Project)
def create_project(project: project_schemas.ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Verificar si el usuario tiene una suscripción activa (aún no lo hemos implementado, pero es un placeholder)
    if not user.is_subscribed:
        raise HTTPException(status_code=403, detail="User does not have an active subscription")
    
    db_project = Project(
        title=project.title,
        description=project.description,
        owner_id=user.id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# Obtener todos los proyectos
@router.get("/", response_model=list[project_schemas.Project])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

# Obtener un proyecto por su ID
@router.get("/{project_id}", response_model=project_schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

# Actualizar un proyecto
@router.put("/{project_id}", response_model=project_schemas.Project)
def update_project(project_id: int, project: project_schemas.ProjectUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Verificar si el usuario es el dueño del proyecto
    if db_project.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You can only update your own projects")

    db_project.title = project.title
    db_project.description = project.description
    db_project.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_project)
    return db_project

# Eliminar un proyecto
@router.delete("/{project_id}", response_model=project_schemas.Project)
def delete_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Verificar si el usuario es el dueño del proyecto
    if db_project.owner_id != user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own projects")

    db.delete(db_project)
    db.commit()
    return db_project
