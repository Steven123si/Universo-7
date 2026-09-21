from pydantic import BaseModel, EmailStr
from typing import Optional, List

# --- Usuarios ---
class UsuarioRegistro(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str

class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Planetas (Entidad Principal) ---
class PlanetaCrear(BaseModel):
    nombre: str
    galaxia: str

class PlanetaRespuesta(BaseModel):
    id: int
    nombre: str
    galaxia: str

# --- Razas (Entidad Dependiente) ---
class RazaCrear(BaseModel):
    nombre: str
    fuerza_base: int
    habilidad_especial: str
    planeta_id: int

class RazaRespuesta(BaseModel):
    id: int
    nombre: str
    fuerza_base: int
    habilidad_especial: str
    planeta_id: int

# --- Modelo para Consulta con JOIN ---
class PlanetaConRazasRespuesta(PlanetaRespuesta):
    razas: List[RazaRespuesta] = []