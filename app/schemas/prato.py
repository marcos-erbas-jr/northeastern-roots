from pydantic import BaseModel

class PratoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    promocao: Optional[bool] = False
    imagem: Optional[str] = None
    unidade_id: int