from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ItemPedidoCreate(BaseModel):
    prato_id: int
    quantidade: int

class PedidoCreate(BaseModel):
    cliente_id: int
    unidade_id: int
    status: str
    itens: List[ItemPedidoCreate]