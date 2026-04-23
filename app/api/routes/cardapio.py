from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login
from app.core.database import SessionLocal
from app.models.prato import Prato
from app.models.unidade import Unidade

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/cardapio")
def pagina_cardapio(request: Request, unidade_id: int = None):

    response = verificar_login(request)
    if response:
        return response

    db = SessionLocal()
    unidades = db.query(Unidade).all()
    if unidade_id:
        pratos = db.query(Prato).filter(Prato.unidade_id == unidade_id).all()
    else:
        pratos = db.query(Prato).all()
    pratos_formatados = []
    for p in pratos:
        pratos_formatados.append({
            "id": p.id,
            "nome": p.nome,
            "preco": p.preco,
            "promocao": "Sim" if p.promocao else "Não",
            "unidade": p.unidade.nome if p.unidade else "-"
        })
    db.close()

    return templates.TemplateResponse(
        name="cardapio.html",
        request=request,
        context={
            "pratos": pratos_formatados,
            "unidades": unidades,
            "role": request.cookies.get("role")
        }
    )