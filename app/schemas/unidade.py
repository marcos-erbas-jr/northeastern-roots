from pydantic import BaseModel

class UnidadeCreate(BaseModel):
    nome: str
    cidade: str
    ativo: bool = True
