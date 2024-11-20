from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    # Relación con el modelo Project
    projects = relationship("Project", back_populates="owner")
