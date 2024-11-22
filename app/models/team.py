from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.services.db import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con el dueño del equipo
    owner = relationship("User", back_populates="owned_teams")

    # Relación con los miembros del equipo
    members = relationship("TeamMember", back_populates="team", cascade="all, delete")
    # Relación con las invitaciones asociadas al equipo
    invitations = relationship("Invitation", back_populates="team", cascade="all, delete")

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    is_active = Column(Boolean, default=True)  # Para verificar si está activo en el equipo

    # Relación con el equipo
    team = relationship("Team", back_populates="members")
    # Relación con el usuario
    user = relationship("User", back_populates="teams")


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    status = Column(String, default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con el equipo
    team = relationship("Team", back_populates="invitations")
    # Relación con el usuario
    user = relationship("User", back_populates="invitations")

