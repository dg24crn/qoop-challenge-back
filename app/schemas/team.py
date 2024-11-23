from pydantic import BaseModel
from datetime import datetime
from typing import List


class TeamBase(BaseModel):
    name: str


class TeamCreate(TeamBase):
    owner_id: int


class TeamResponse(TeamBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class InvitationBase(BaseModel):
    team_id: int
    user_id: int


class InvitationResponse(BaseModel):
    id: int
    team_id: int
    user_id: int
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class TeamMemberResponse(BaseModel):
    id: int
    team_id: int
    user_id: int
    is_active: bool

    class Config:
        orm_mode = True


class AddMemberRequest(BaseModel):
    user_id: int


class RemoveMemberResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True
