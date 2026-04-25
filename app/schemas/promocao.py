from pydantic import BaseModel

class PromocaoCreate(BaseModel):
    desconto: float = Field(gt=0, le=100)
    ativo: bool = True
    unidade_id: int
    prato_id: int