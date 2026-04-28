from app.core.database import SessionLocal
from app.core.database import Base, engine
from app.core.security import gerar_hash
from app.models import *

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

    ingredientes_lista = [
        "Feijão fradinho",
        "Cebola",
        "Sal",
        "Azeite de dendê",
        "Camarão seco",
        "Peixe",
        "Tomate",
        "Pimentão",
        "Leite de coco",
        "Alho",
        "Pão",
        "Amendoim",
        "Castanha de caju",
    ]

    receitas = [
        ("Acarajé", "campos", "Feijão fradinho", 100),
        ("Acarajé", "campos", "Cebola", 20),
        ("Acarajé", "campos", "Sal", 5),
        ("Acarajé", "campos", "Azeite de dendê", 30),
        ("Acarajé", "campos", "Camarão seco", 20),

        ("Vatapá", "campos", "Pão", 80),
        ("Vatapá", "campos", "Leite de coco", 100),
        ("Vatapá", "campos", "Amendoim", 30),
        ("Vatapá", "campos", "Castanha de caju", 30),
        ("Vatapá", "campos", "Camarão seco", 20),
        ("Vatapá", "campos", "Azeite de dendê", 20),
        ("Vatapá", "campos", "Cebola", 10),
        ("Vatapá", "campos", "Alho", 5),

        ("Moqueca", "rio", "Peixe", 200),
        ("Moqueca", "rio", "Tomate", 50),
        ("Moqueca", "rio", "Cebola", 30),
        ("Moqueca", "rio", "Pimentão", 40),
        ("Moqueca", "rio", "Leite de coco", 100),
        ("Moqueca", "rio", "Azeite de dendê", 30),
        ("Moqueca", "rio", "Alho", 10),
        ("Moqueca", "rio", "Sal", 5),
    ]

    estoque = {
        "campos": [
            ("Feijão fradinho", 500),
            ("Cebola", 300),
            ("Sal", 200),
            ("Azeite de dendê", 200),
            ("Camarão seco", 150),
            ("Pão", 100),
            ("Leite de coco", 200),
            ("Amendoim", 100),
            ("Castanha de caju", 100),
            ("Alho", 100) ],
        "rio": [("Peixe", 400),
            ("Tomate", 300),
            ("Cebola", 200),
            ("Pimentão", 200),
            ("Leite de coco", 300),
            ("Azeite de dendê", 200),
            ("Alho", 100),
            ("Sal", 100)]
    }

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

    clientes = [
        {
            "nome": "João Silva",
            "email": "joao@email.com",
            "telefone": "22999999999"
        },
        {
            "nome": "Maria Souza",
            "email": "maria@email.com",
            "telefone": "22988888888"
        }
    ]

    pedidos = [
        {
            "cliente": "joao@email.com",
            "unidade": "campos",
            "status": "pendente",
            "canal": "app",
            "itens": [
                {"prato": "acaraje", "quantidade": 2},
                {"prato": "vatapa", "quantidade": 1}
            ]
        },
        {
            "cliente": None,
            "unidade": "rio",
            "status": "preparando",
            "canal": "balcao",
            "itens": [
                {"prato": "moqueca", "quantidade": 1}
            ]
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

    prato_vatapa = db.query(Prato).filter(
        Prato.nome == "Vatapá",
        Prato.unidade_id == unidade_campos.id
    ).first()

    mapa_pratos = {
        "acaraje": prato_acaraje,
        "moqueca": prato_moqueca,
        "vatapa": prato_vatapa
    }

    mapa_ingredientes = {}

    for nome in ingredientes_lista:
        ing = db.query(Ingrediente).filter(Ingrediente.nome == nome).first()

        if not ing:
            ing = Ingrediente(nome=nome)
            db.add(ing)
            db.flush()

        mapa_ingredientes[nome.lower()] = ing

    db.commit()

    for prato_nome, unidade_key, ing_nome, qtd in receitas:
        unidade = mapa_unidades[unidade_key]
        prato = db.query(Prato).filter(
            Prato.nome == prato_nome,
            Prato.unidade_id == unidade.id).first()
        ingrediente = mapa_ingredientes[ing_nome.lower()]
        existe = db.query(Receita).filter(
            Receita.prato_id == prato.id,
            Receita.ingrediente_id == ingrediente.id
        ).first()
        if not existe:
            db.add(Receita(
                prato_id=prato.id,
                ingrediente_id=ingrediente.id,
                quantidade=qtd
            ))
    db.commit()

    for unidade_key, itens in estoque.items():
        unidade = mapa_unidades[unidade_key]

        for nome_ing, qtd in itens:
            ingrediente = mapa_ingredientes[nome_ing.lower()]
            existe = db.query(Estoque).filter(
                Estoque.unidade_id == unidade.id,
                Estoque.ingrediente_id == ingrediente.id
            ).first()

            if not existe:
                db.add(Estoque(
                    unidade_id=unidade.id,
                    ingrediente_id=ingrediente.id,
                    quantidade=qtd
                ))

    db.commit()

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

    mapa_clientes = {}

    for c in clientes:
        existe = db.query(Cliente).filter(Cliente.email == c["email"]).first()
        if not existe:
            novo = Cliente(
                nome=c["nome"],
                email=c["email"],
                telefone=c["telefone"]
            )
            db.add(novo)
            db.flush()
            mapa_clientes[c["email"]] = novo
        else:
            mapa_clientes[c["email"]] = existe

    db.commit()

    from datetime import datetime

    for p in pedidos:
        cliente = mapa_clientes.get(p.get("cliente"))
        unidade = mapa_unidades.get(p["unidade"])
        if not unidade:
            print("Erro: unidade não encontrada!", p)
            continue

        novo_pedido = Pedido(
            cliente_id=cliente.id if cliente else None,
            unidade_id=unidade.id,
            status=p["status"],
            canal=p["canal"],
            data=datetime.now()
        )

        db.add(novo_pedido)
        db.flush()

        for item in p["itens"]:
            prato = mapa_pratos.get(item["prato"])
            if not prato:
                print("ERRO: item ignorado ->", item)
                continue
            db.add(ItemPedido(
                pedido_id=novo_pedido.id,
                prato_id=prato.id,
                quantidade=item["quantidade"]
            ))

    db.commit()


    db.close()
    print("Seed executado")

if __name__ == "__main__":
    seed()