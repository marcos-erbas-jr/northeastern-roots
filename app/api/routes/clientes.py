from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login
from app.core.database import SessionLocal
from app.models.cliente import Cliente

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def classificar_fidelizacao(qtd_pedidos):
    if qtd_pedidos >= 10:
        return "sim"
    return "nao"

@router.get("/clientes")
def pagina_clientes(request: Request):

    response = verificar_login(request)
    if response:
        return response

    db = SessionLocal()
    clientes = db.query(Cliente).all()
    clientes_formatados = []

    for c in clientes:
        total_pedidos = len(c.pedidos)

        clientes_formatados.append({
            "id": c.id,
            "nome": c.nome,
            "email": c.email,
            "telefone": c.telefone,
            "pedidos": total_pedidos,
            "fidelizacao": classificar_fidelizacao(total_pedidos),
        })

    db.close()

    return templates.TemplateResponse(
        name="clientes.html",
        request=request,
        context={
            "clientes": clientes_formatados,
            "role": request.cookies.get("role")
        }
    )