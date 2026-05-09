from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login, verificar_permissao
from app.core.database import SessionLocal
from app.models.promocao import Promocao
from app.models.unidade import Unidade
from app.models.prato import Prato
from fastapi.responses import RedirectResponse

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

@router.get("/promocao/nova")
def nova_promocao(request: Request):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    unidades = db.query(Unidade).all()
    pratos = db.query(Prato).filter(
        Prato.ativo == True
    ).all()
    db.close()
    return templates.TemplateResponse(
        name="promocao_form.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "unidades": unidades,
            "pratos": pratos,
            "erro": None
        }
    )

@router.post("/promocao/criar")
def criar_promocao(
    request: Request,
    desconto: float = Form(...),
    unidade_id: int = Form(...),
    prato_id: int = Form(...)):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    nova = Promocao(
        desconto=desconto,
        ativo=True,
        unidade_id=unidade_id,
        prato_id=prato_id
    )
    db.add(nova)
    try:
        db.commit()
    except Exception:
        db.rollback()
        unidades = db.query(Unidade).all()
        pratos = db.query(Prato).filter(
            Prato.ativo == True
        ).all()
        db.close()
        return templates.TemplateResponse(
            name="promocao_form.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "unidades": unidades,
                "pratos": pratos,
                "erro": "Erro ao criar promoção"
            }
        )
    db.close()
    return RedirectResponse(
        "/promocao",
        status_code=303
    )

@router.get("/promocao/editar/{id}")
def editar_promocao(request: Request, id: int):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    promocao = db.query(Promocao).filter(Promocao.id == id).first()
    unidades = db.query(Unidade).all()
    pratos = db.query(Prato).filter(
        Prato.ativo == True
    ).all()
    db.close()
    return templates.TemplateResponse(
        name="editar_promocao.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "promocao": promocao,
            "unidades": unidades,
            "pratos": pratos,
            "erro": None
        }
    )

@router.post("/promocao/atualizar/{id}")
def atualizar_promocao(
    request: Request,
    id: int,
    desconto: float = Form(...),
    unidade_id: int = Form(...),
    prato_id: int = Form(...),
    ativo: str = Form(None)):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    promocao = db.query(Promocao).filter(
        Promocao.id == id
    ).first()
    promocao.desconto = desconto
    promocao.unidade_id = unidade_id
    promocao.prato_id = prato_id
    promocao.ativo = True if ativo == "on" else False

    try:
        db.commit()
    except Exception:
        db.rollback()
        unidades = db.query(Unidade).all()
        pratos = db.query(Prato).filter(
            Prato.ativo == True
        ).all()
        return templates.TemplateResponse(
            name="editar_promocao.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "promocao": promocao,
                "unidades": unidades,
                "pratos": pratos,
                "erro": "Erro ao atualizar promoção"
            }
        )
    db.close()
    return RedirectResponse(
        "/promocao",
        status_code=303
    )

@router.get("/promocao/excluir/{id}")
def excluir_promocao(request: Request, id: int):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    promocao = db.query(Promocao).filter(
        Promocao.id == id
    ).first()
    if promocao:
        db.delete(promocao)
        db.commit()
    db.close()
    return RedirectResponse(
        "/promocao",
        status_code=303)