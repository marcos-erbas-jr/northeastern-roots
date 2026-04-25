from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    #quantidade = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    unidade = relationship("Unidade", back_populates="ingredientes")
    #prato_id = Column(Integer, ForeignKey("pratos.id"))
    #prato = relationship("Prato", back_populates="ingredientes")
    receitas = relationship("Receita", back_populates="ingrediente")
    estoques = relationship("Estoque", back_populates="ingrediente")