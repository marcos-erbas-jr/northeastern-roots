from pydantic import BaseModel

class PratoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    ativo: bool = True
    #promocao: Optional[bool] = False
    unidade_id: int