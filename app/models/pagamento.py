from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Pagamento(Base):
    __tablename__ = "pagamentos"
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    valor = Column(Float)
    status = Column(String)
    transacao_id = Column(String)
    pedido = relationship("Pedido", back_populates="pagamento")