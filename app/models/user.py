from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from app.services.db import Base
from datetime import datetime

# Configuración para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)

    # Campos relacionados con suscripciones
    is_subscribed = Column(Boolean, default=False, nullable=False)
    subscription_expiration = Column(DateTime, nullable=True)

    # Relación con Project
    projects = relationship("Project", back_populates="owner")
    # Relación con Task
    tasks = relationship("Task", back_populates="assigned_to")

    # Relación con equipos que posee el usuario
    owned_teams = relationship("Team", back_populates="owner", cascade="all, delete-orphan")
    # Relación con los equipos a los que pertenece el usuario
    teams = relationship("TeamMember", back_populates="user", cascade="all, delete")
    # Relación con las invitaciones enviadas/recibidas
    invitations = relationship("Invitation", back_populates="user", cascade="all, delete")

    # Método para verificar contraseña
    def verify_password(self, plain_password: str) -> bool:
        """
        Verifica si la contraseña ingresada coincide con la almacenada.
        """
        return pwd_context.verify(plain_password, self.password)

    # Método para hashear contraseña
    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Hashea una contraseña para guardarla de forma segura.
        """
        return pwd_context.hash(plain_password)

    # Método para verificar si la suscripción es válida
    def is_subscription_valid(self) -> bool:
        """
        Verifica si la suscripción del usuario es válida con base en la fecha de expiración.
        """
        if not self.is_subscribed or not self.subscription_expiration:
            return False
        return datetime.utcnow() < self.subscription_expiration
