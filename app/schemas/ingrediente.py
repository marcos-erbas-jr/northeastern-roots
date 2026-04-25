from pydantic import BaseModel

class EstoqueCreate(BaseModel):
    nome: str
    quantidade: float
    unidade_id: int
    prato_id: int
