from pydantic import BaseModel

# Esquema para crear un usuario (input)
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

# Esquema para responder datos de usuario (output)
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True

# Esquema para manejar el login (input)
class UserLogin(BaseModel):
    email: str
    password: str

# Esquema para responder con el token (output)
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
