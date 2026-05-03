from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login, verificar_permissao
from app.core.database import SessionLocal
from app.models.pedido import Pedido
from app.models.unidade import Unidade
from app.core.mock import processar_pagamento_mock
from app.models.itemPedido import ItemPedido
from app.models.prato import Prato
from app.models.pagamento import Pagamento
from datetime import datetime
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def calcular_total(pedido):
    total = 0
    for item in pedido.itens:
        if item.prato:
            total += item.quantidade * item.prato.preco
    return round(total, 2)

def formatar_canal(canal):
    mapa = {
        "app": "Aplicativo",
        "totem": "Totem",
        "balcao": "Balcão",
        "pickup": "Retirada"
    }
    return mapa.get(canal, canal)

@router.get("/pedido")
def escolher_unidade(request: Request):

    db = SessionLocal()
    unidades = db.query(Unidade).all()
    db.close()

    return templates.TemplateResponse(
        "restaurante.html",
        {
            "request": request,
            "unidades": unidades
        }
    )

@router.get("/pedidos")
def pagina_pedidos(request: Request, unidade_id: int = None):

    response = verificar_login(request)
    if response:
        return response

    perm = verificar_permissao(request, ["admin", "atendente", "cozinha"])
    if perm:
        return perm

    db = SessionLocal()
    unidades = db.query(Unidade).all()

    role = request.cookies.get("role")
    unidade_usuario = request.cookies.get("unidade_id")

    if role == "admin":
        if unidade_id:
            pedidos = db.query(Pedido).filter(
                Pedido.unidade_id == unidade_id).all()
        else:
            pedidos = db.query(Pedido).all()
    else:
        pedidos = db.query(Pedido).filter(
            Pedido.unidade_id == int(unidade_usuario)).all()

    pedidos_formatados = []

    for p in pedidos:
        nomes_pratos = []
        quantidade_total = 0

        for item in p.itens:
            if item.prato:
                nomes_pratos.append(item.prato.nome)
                quantidade_total += item.quantidade

        pedidos_formatados.append({
            "id": p.id,
            "pratos": ", ".join(nomes_pratos),
            "quantidade": quantidade_total,
            "total": calcular_total(p),
            "status": p.status,
            "cliente": p.cliente.nome if p.cliente else "-",
            "unidade": p.unidade.nome if p.unidade else "-",
            "canal": formatar_canal(p.canal)
        })

    db.close()

    return templates.TemplateResponse(
        name="pedidos.html",
        request=request,
        context={
            "pedidos": pedidos_formatados,
            "unidades": unidades,
            "role": request.cookies.get("role")
        }
    )

@router.get("/criar_pedido")
def tela_criar_pedido(request: Request):
    response = verificar_login(request)
    if response:
        return response

    db = SessionLocal()

    role = request.cookies.get("role")
    unidade_usuario = request.cookies.get("unidade_id")

    '''if role == "admin":
        unidades = db.query(Unidade).all()
        pratos = db.query(Prato).all()
        unidade_id = None
    else:
        unidade_id = int(unidade_usuario)
        unidades = None
        pratos = db.query(Prato).filter(
            Prato.unidade_id == unidade_id).all()'''
    unidade_id = int(unidade_usuario)
    unidades = None
    pratos = db.query(Prato).filter(
        Prato.unidade_id == unidade_id).all()

    db.close()

    return templates.TemplateResponse(
        name="criar_pedido.html",
        request=request,
        context={
            "pratos": pratos,
            "unidades": unidades,
            "unidade_id": unidade_id,
            "role": role
        }
    )

@router.post("/pedidos/criar")
def criar_pedido(
    request: Request,
    unidade_id: int = Form(...),
    canal: str = Form(...)
):
    response = verificar_login(request)
    if response:
        return response

    db = SessionLocal()

    usuario_id = request.cookies.get("user_id")
    usuario_id = int(usuario_id) if usuario_id else None

    novo_pedido = Pedido(
        unidade_id=unidade_id,
        status="pendente",
        canal=canal,
        data=datetime.now(),
        usuario_id = usuario_id
    )

    db.add(novo_pedido)
    db.flush()

    prato = db.query(Prato).filter(Prato.unidade_id == unidade_id).first()

    db.add(ItemPedido(
        pedido_id=novo_pedido.id,
        prato_id=prato.id,
        quantidade=1
    ))

    db.flush()

    #total = calcular_total(novo_pedido)
    total = prato.preco * 1

    resultado = processar_pagamento_mock(total)

    pagamento = Pagamento(
        pedido_id=novo_pedido.id,
        valor=total,
        status=resultado["status"],
        transacao_id=resultado["transacao_id"]
    )

    db.add(pagamento)
    novo_pedido.status = (
        "pago" if resultado["status"] == "aprovado" else "recusado"
    )

    db.commit()
    db.close()

    return RedirectResponse("/pedidos", status_code=303)

@router.post("/pedidos/criar_com_itens")
async def criar_pedido_com_itens(request: Request):
    data = await request.json()
    db = SessionLocal()
    unidade_id = data.get("unidade_id")
    itens = data.get("itens", [])
    usuario_id = request.cookies.get("user_id")
    usuario_id = int(usuario_id) if usuario_id else None

    if not unidade_id or not itens:
        db.close()
        return {"erro": "Dados inválidos"}
    novo_pedido = Pedido(
        unidade_id=unidade_id,
        canal="balcao",
        status="pendente",
        data=datetime.now(),
        usuario_id=usuario_id
    )

    db.add(novo_pedido)
    db.flush()

    total = 0

    for item in itens:
        prato = db.query(Prato).filter(
            Prato.id == item["id"]
        ).first()

        if not prato:
            continue
        quantidade = item.get("quantidade", 1)

        db.add(ItemPedido(
            pedido_id=novo_pedido.id,
            prato_id=prato.id,
            quantidade=quantidade
        ))

        total += prato.preco * quantidade

    resultado = processar_pagamento_mock(total)
    pagamento = Pagamento(
        pedido_id=novo_pedido.id,
        valor=total,
        status=resultado["status"],
        transacao_id=resultado["transacao_id"]
    )

    db.add(pagamento)
    novo_pedido.status = (
        "pago" if resultado["status"] == "aprovado"
        else "recusado"
    )
    db.commit()
    db.close()
    return {"status": "ok"}

@router.post("/pedido_publico")
async def pedido_publico(request: Request):
    data = await request.json()
    db = SessionLocal()
    unidade_id = data.get("unidade_id")

    itens = data.get("itens", [])

    if not unidade_id or not itens:
        db.close()
        return {"erro": "Dados inválidos"}

    novo_pedido = Pedido(
        unidade_id=unidade_id,
        canal="totem",
        status="pendente",
        data=datetime.now()
    )

    db.add(novo_pedido)
    db.flush()
    total = 0

    for item in itens:
        prato = db.query(Prato).filter(
            Prato.id == item["id"]
        ).first()

        if not prato:
            continue

        quantidade = item.get("quantidade", 1)

        db.add(ItemPedido(
            pedido_id=novo_pedido.id,
            prato_id=prato.id,
            quantidade=quantidade
        ))

        total += prato.preco * quantidade

    resultado = processar_pagamento_mock(total)
    pagamento = Pagamento(
        pedido_id=novo_pedido.id,
        valor=total,
        status=resultado["status"],
        transacao_id=resultado["transacao_id"]
    )

    db.add(pagamento)
    novo_pedido.status = (
        "pago" if resultado["status"] == "aprovado"
        else "recusado"
    )
    db.commit()
    db.close()
    return {
        "status": "ok",
        "pagamento": resultado
    }