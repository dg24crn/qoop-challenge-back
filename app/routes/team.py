from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.team import Team, TeamMember, Invitation
from app.schemas.team import (
    TeamCreate,
    TeamResponse,
    InvitationBase,
    InvitationResponse,
    TeamMemberResponse,
    AddMemberRequest,
    RemoveMemberResponse
)
from app.models.user import User
from app.services.db import get_db
from app.services.dependencies import get_current_user

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/", response_model=TeamResponse)
def create_team(team: TeamCreate, db: Session = Depends(get_db)):
    new_team = Team(name=team.name, owner_id=team.owner_id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


@router.post("/{team_id}/invite", response_model=InvitationResponse)
def invite_member(
    team_id: int, invitation: InvitationBase, db: Session = Depends(get_db)
):
    existing_invitation = (
        db.query(Invitation)
        .filter(Invitation.team_id == team_id, Invitation.user_id == invitation.user_id)
        .first()
    )
    if existing_invitation:
        raise HTTPException(status_code=400, detail="User already invited to the team.")

    new_invitation = Invitation(team_id=team_id, user_id=invitation.user_id)
    db.add(new_invitation)
    db.commit()
    db.refresh(new_invitation)
    return new_invitation


@router.get("/{team_id}/members", response_model=list[dict])
def list_team_members(team_id: int, db: Session = Depends(get_db)):
    """
    List all members of a specific team, including user details.
    """
    # Verificar si el equipo existe
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Realizar el JOIN entre team_members y users
    members = (
        db.query(TeamMember, User)
        .join(User, TeamMember.user_id == User.id)
        .filter(TeamMember.team_id == team_id)
        .all()
    )

    # Formatear los datos para la respuesta
    response = [
        {
            "id": member.TeamMember.id,
            "team_id": member.TeamMember.team_id,
            "user_id": member.TeamMember.user_id,
            "is_active": member.TeamMember.is_active,
            "first_name": member.User.first_name,
            "last_name": member.User.last_name,
            "email": member.User.email,
        }
        for member in members
    ]

    return response


@router.post("/{team_id}/add_member", response_model=dict)
def add_member_to_team(
    team_id: int,
    request: AddMemberRequest,
    db: Session = Depends(get_db),
):
    # Verificar si el equipo existe
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Verificar si el usuario existe
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verificar si el usuario ya es miembro del equipo
    existing_member = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == request.user_id)
        .first()
    )
    if existing_member:
        raise HTTPException(
            status_code=400, detail=f"User {user.first_name} is already a member of the team."
        )

    # Agregar el miembro al equipo
    team_member = TeamMember(team_id=team_id, user_id=request.user_id)
    db.add(team_member)
    db.commit()
    db.refresh(team_member)

    return {"message": f"User {request.user_id} added to team {team_id} successfully"}



@router.get("/by_owner/{owner_id}", response_model=TeamResponse)
def get_team_by_owner(owner_id: int, db: Session = Depends(get_db)):
    """
    Obtener el equipo asociado al owner_id proporcionado.
    """
    team = db.query(Team).filter(Team.owner_id == owner_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="No team found for this user.")
    return team


@router.delete("/{team_id}/remove_member/{user_id}", response_model=dict)
def remove_member_from_team(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    # Verificar si el equipo existe
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Verificar si el miembro está en el equipo
    team_member = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id)
        .first()
    )
    if not team_member:
        raise HTTPException(status_code=404, detail="User is not a member of this team.")

    # Obtener el usuario
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Eliminar el miembro
    db.delete(team_member)
    db.commit()

    return {
        "message": f"User {user.first_name} removed from team {team.name} successfully"
    }
