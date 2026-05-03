from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    role = Column(String)
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    unidade = relationship("Unidade", back_populates="usuarios")
    pedidos = relationship("Pedido", back_populates="usuario")