from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login
from app.core.database import SessionLocal
from app.models.estoque import Estoque
from app.models.unidade import Unidade

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def classificar_estoque(qtd):
    if qtd <= 50:
        return "baixo"
    elif qtd <= 150:
        return "medio"
    return "alto"

@router.get("/estoque")
def pagina_estoque(request: Request, unidade_id: int = None):

    response = verificar_login(request)
    if response:
        return response
    db = SessionLocal()
    unidades = db.query(Unidade).all()

    if unidade_id:
        estoques = db.query(Estoque).filter(
            Estoque.unidade_id == unidade_id
        ).all()
    else:
        estoques = db.query(Estoque).all()

    estoques_formatados = []

    for e in estoques:
        estoques_formatados.append({
            "id": e.id,
            "ingrediente": e.ingrediente.nome if e.ingrediente else "-",
            "unidade": e.unidade.nome if e.unidade else "-",
            "quantidade": e.quantidade,
            "status": classificar_estoque(e.quantidade)
        })
    db.close()

    return templates.TemplateResponse(
        name="estoque.html",
        request=request,
        context={
            "estoques": estoques_formatados,
            "unidades": unidades,
            "role": request.cookies.get("role")
        }
    )