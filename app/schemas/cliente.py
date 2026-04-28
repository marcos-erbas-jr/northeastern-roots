from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None