from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login, verificar_permissao
from app.core.database import SessionLocal
from app.models.promocao import Promocao
from app.models.unidade import Unidade

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/promocao")
def pagina_promocoes(request: Request, unidade_id: int = None):

    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm

    db = SessionLocal()
    unidades = db.query(Unidade).all()

    if unidade_id:
        promocoes = db.query(Promocao).filter(
            Promocao.unidade_id == unidade_id
        ).all()
    else:
        promocoes = db.query(Promocao).all()

    promocoes_formatadas = []

    for promo in promocoes:
        if not promo.prato:
            continue
        preco_original = promo.prato.preco
        desconto = promo.desconto
        preco_final = preco_original * (1 - desconto / 100)

        promocoes_formatadas.append({
            "id": promo.id,
            "prato": promo.prato.nome,
            "preco_fixo": round(preco_original, 2),
            "desconto": desconto,
            "preco_promo": round(preco_final, 2)
        })

    db.close()

    return templates.TemplateResponse(
        name="promocao.html",
        request=request,
        context={
            "promocoes": promocoes_formatadas,
            "unidades": unidades,
            "role": request.cookies.get("role")
        }
    )