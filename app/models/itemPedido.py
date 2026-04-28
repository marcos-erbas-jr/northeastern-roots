from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    id = Column(Integer, primary_key=True)
    quantidade = Column(Integer, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    pedido = relationship("Pedido", back_populates="itens")
    prato_id = Column(Integer, ForeignKey("pratos.id"))
    prato = relationship("Prato")