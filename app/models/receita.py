from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Receita(Base):
    __tablename__ = "receitas"
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Float, nullable=False)
    prato_id = Column(Integer, ForeignKey("pratos.id"))
    prato = relationship("Prato", back_populates="receitas")
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"))
    ingrediente = relationship("Ingrediente", back_populates="receitas")