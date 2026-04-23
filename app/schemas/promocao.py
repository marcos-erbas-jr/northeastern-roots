from pydantic import BaseModel

class PromocaoCreate(BaseModel):
    desconto: float = Field(gt=0, le=100)
    ativo: bool = True
    unidade_id: int
    prato_id: int

class Promocao(Base):
    __tablename__ = "promocoes"
    id = Column(Integer, primary_key=True, index=True)
    desconto = Column(Float, nullable=False)
    ativo = Column(Boolean, default=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"))
    unidade = relationship("Unidade", back_populates="promocoes")
    prato_id = Column(Integer, ForeignKey("pratos.id"))
    prato = relationship("Prato", back_populates="promocoes")