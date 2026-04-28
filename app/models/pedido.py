from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True)
    data = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=True)
    cliente = relationship("Cliente", back_populates="pedidos")
    canal = Column(Enum("app", "totem", "balcao", "pickup", name="canal_pedido"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    unidade = relationship("Unidade")
    itens = relationship("ItemPedido", back_populates="pedido")