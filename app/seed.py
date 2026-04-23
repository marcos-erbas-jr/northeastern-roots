from app.core.database import SessionLocal
from app.core.database import Base, engine
from app.models.usuario import Usuario
from app.models.unidade import Unidade
from app.models.prato import Prato
from app.models.promocao import Promocao
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
            "unidade": "campos"
        },
        {
            "nome": "Vatapá",
            "descricao": "Creme feito com farinha de rosca ou fubá, castanha de caju, pimenta, leite de coco, amendoim, pão, azeite de dendê e camarão.",
            "preco": 23.50,
            "unidade": "campos"
        },
        {
            "nome": "Moqueca",
            "descricao": "Consiste em peixe cozinho (pode ser cação) com outros frutos-do-mar como camarão, além de temperos. ",
            "preco": 45.0,
            "unidade": "rio"
        }
    ]

    promocoes = [
        {
            "desconto": 10,
            "unidade": "campos",
            "prato": "acaraje"
        },
        {
            "desconto": 23,
            "unidade": "rio",
            "prato": "moqueca"
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
                #promocao=p["promocao"],
                unidade=unidade
            )
            db.add(novo)

    db.commit()
    prato_acaraje = db.query(Prato).filter(
        Prato.nome == "Acarajé",
        Prato.unidade_id == unidade_campos.id).first()

    prato_moqueca = db.query(Prato).filter(
        Prato.nome == "Moqueca",
        Prato.unidade_id == unidade_rio.id).first()

    mapa_pratos = {
        "acaraje": prato_acaraje,
        "moqueca": prato_moqueca
    }

    for p in promocoes:
        unidade = mapa_unidades.get(p.get("unidade"))
        prato = mapa_pratos.get(p.get("prato"))

        if not unidade or not prato:
            print("ERRO: promoção ignorada ->", p)
            continue
        existe = db.query(Promocao).filter(
            Promocao.prato_id == prato.id,
            Promocao.unidade_id == unidade.id
        ).first()
        if not existe:
            novo = Promocao(
                desconto=p["desconto"],
                unidade=unidade,
                prato=prato
            )
            db.add(novo)


    db.commit()


    db.close()
    print("Seed executado")

if __name__ == "__main__":
    seed()