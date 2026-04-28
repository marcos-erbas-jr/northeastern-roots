from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login
from app.core.database import SessionLocal
from app.models.pedido import Pedido
from app.models.unidade import Unidade

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

@router.get("/pedidos")
def pagina_pedidos(request: Request, unidade_id: int = None):

    response = verificar_login(request)
    if response:
        return response

    db = SessionLocal()
    unidades = db.query(Unidade).all()

    # ✅ FILTRO CORRETO
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