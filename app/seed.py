from app.core.database import SessionLocal
from app.core.database import Base, engine
from app.models.usuario import Usuario
from app.models.unidade import Unidade
from app.core.security import gerar_hash

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    usuarios = [
        {
            "nome": "Admin",
            "email": "admin@raizesdonordeste.com",
            "senha": "12345678",
            "role": "admin",
            "unidade": "campos"
        },
        {
            "nome": "Atendente",
            "email": "atendente@raizesdonordeste.com",
            "senha": "12345678",
            "role": "atendente",
            "unidade": "rio"
        },
        {
            "nome": "Cozinha",
            "email": "cozinha@raizesdonordeste.com",
            "senha": "123456",
            "role": "cozinha",
            "unidade": "campos"
        }
    ]

    unidades = [
        {
            "nome": "Unid.Campos",
            "cidade": "Campos dos Goytacazes",
        },
        {
            "nome": "Unid.Rio",
            "cidade": "Rio de Janeiro",
        }
    ]

    for unid in unidades:
        existe = db.query(Unidade).filter(Unidade.nome == unid["nome"]).first()
        if not existe:
            novo = Unidade(
                nome=unid["nome"],
                cidade=unid["cidade"]
            )
            db.add(novo)

    db.commit()

    unidade_campos = db.query(Unidade).filter(Unidade.nome == "Unid.Campos").first()
    unidade_rio = db.query(Unidade).filter(Unidade.nome == "Unid.Rio").first()

    mapa_unidades = {
        "campos": unidade_campos,
        "rio": unidade_rio
    }
    for u in usuarios:
        unidade = mapa_unidades.get(u.get("unidade"))

        novo = Usuario(
            nome=u["nome"],
            email=u["email"],
            senha=gerar_hash(u["senha"]),
            role=u["role"],
            unidade=unidade
        )
        db.add(novo)

    db.commit()


    db.commit()
    db.close()
    print("Seed executado")

if __name__ == "__main__":
    seed()