from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prato(Base):
    __tablename__ = "pratos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    promocao = Column(Boolean, default=False)
    imagem = Column(String)
    ativo = Column(Integer, default=1)
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    unidade = relationship("Unidade", back_populates="pratos")