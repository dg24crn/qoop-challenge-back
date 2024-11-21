from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.services.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    completed = Column(Boolean, default=False)

    project = relationship("Project", back_populates="tasks")
    assigned_to = relationship("User", back_populates="tasks")
