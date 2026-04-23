from app.core.database import SessionLocal
from app.core.database import Base, engine
from app.models.usuario import Usuario
from app.models.unidade import Unidade
from app.models.prato import Prato
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

    pratos = [
        {
            "nome": "Acarajé",
            "descricao": "Bolinho frito no azeite de dendê, feito com feijão fradinho, sal, alho, gengibre, cebola e recheado com camarão",
            "preco": 15.0,
            "promocao": False,
            "unidade": "campos"
        },
        {
            "nome": "Vatapá",
            "descricao": "Creme feito com farinha de rosca ou fubá, castanha de caju, pimenta, leite de coco, amendoim, pão, azeite de dendê e camarão.",
            "preco": 23.50,
            "promocao": False,
            "unidade": "campos"
        },
        {
            "nome": "Moqueca",
            "descricao": "Consiste em peixe cozinho (pode ser cação) com outros frutos-do-mar como camarão, além de temperos. ",
            "preco": 45.0,
            "promocao": False,
            "unidade": "rio"
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

    for p in pratos:
        unidade = mapa_unidades.get(p.get("unidade"))

        existe = db.query(Prato).filter(
            Prato.nome == p["nome"],
            Prato.unidade_id == unidade.id
        ).first()

        if not existe:
            novo = Prato(
                nome=p["nome"],
                descricao=p["descricao"],
                preco=p["preco"],
                promocao=p["promocao"],
                unidade=unidade
            )
            db.add(novo)


    db.commit()
    db.close()
    print("Seed executado")

if __name__ == "__main__":
    seed()