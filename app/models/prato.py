from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prato(Base):
    __tablename__ = "pratos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    unidade = relationship("Unidade", back_populates="pratos")
    promocoes = relationship("Promocao", back_populates="prato")