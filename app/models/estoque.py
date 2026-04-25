from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Estoque(Base):
    __tablename__ = "estoques"
    id = Column(Integer, primary_key=True)
    quantidade = Column(Float, nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"))
    unidade = relationship("Unidade", back_populates="estoques")
    ingrediente = relationship("Ingrediente", back_populates="estoques")