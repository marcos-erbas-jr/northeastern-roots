from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login
from app.core.database import SessionLocal
from app.models.pedido import Pedido
from app.models.unidade import Unidade
from app.core.mock import processar_pagamento_mock
from app.models.itemPedido import ItemPedido
from app.models.prato import Prato
from app.models.pagamento import Pagamento
from datetime import datetime

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

    db = SessionLocal()
    unidades = db.query(Unidade).all()

    if unidade_id:
        pedidos = db.query(Pedido).filter(
            Pedido.unidade_id == unidade_id
        ).all()
    else:
        pedidos = db.query(Pedido).all()

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

    novo_pedido = Pedido(
        unidade_id=unidade_id,
        status="pendente",
        canal=canal,
        data=datetime.now()
    )

    db.add(novo_pedido)
    db.flush()

    prato = db.query(Prato).first()

    db.add(ItemPedido(
        pedido_id=novo_pedido.id,
        prato_id=prato.id,
        quantidade=1
    ))

    db.flush()

    total = calcular_total(novo_pedido)

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