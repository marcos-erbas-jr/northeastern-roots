from pydantic import BaseModel

class ReceitaCreate(BaseModel):
    prato_id: int
    ingrediente_id: int
    quantidade: float