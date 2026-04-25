from pydantic import BaseModel

class EstoqueCreate(BaseModel):
    unidade_id: int
    ingrediente_id: int
    quantidade: float