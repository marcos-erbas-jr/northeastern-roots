from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class Unidade(Base):
    __tablename__ = "unidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    cidade = Column(String)
    ativo = Column(Boolean, default=True)
    usuarios = relationship("Usuario", back_populates="unidade")