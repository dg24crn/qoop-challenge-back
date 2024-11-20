from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    username: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str  # Asegúrate de agregar el campo de la contraseña

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str
