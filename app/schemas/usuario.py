from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    role: str
    unidade_id: int

class UsuarioLogin(BaseModel):
    email: str
    senha: str