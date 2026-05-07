from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login, verificar_permissao
from app.core.database import SessionLocal
from app.models.prato import Prato
from app.models.unidade import Unidade
from app.models.promocao import Promocao
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/cardapio")
def pagina_cardapio(request: Request, unidade_id: int = None):

    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin","cozinha", "atendente"])
    if perm:
        return perm

    db = SessionLocal()
    unidades = db.query(Unidade).all()

    role = request.cookies.get("role")
    unidade_usuario = request.cookies.get("unidade_id")

    if role == "admin":
        if unidade_id:
            pratos = db.query(Prato).filter(
                Prato.unidade_id == unidade_id
            ).all()
            promocoes = db.query(Promocao).filter(
                Promocao.unidade_id == unidade_id
            ).all()
        else:
            pratos = db.query(Prato).all()
            promocoes = db.query(Promocao).all()
    else:
        pratos = db.query(Prato).filter(
            Prato.unidade_id == int(unidade_usuario)
        ).all()
        promocoes = db.query(Promocao).filter(
            Promocao.unidade_id == int(unidade_usuario)
        ).all()

    mapa_promocoes = {
        (p.prato_id, p.unidade_id): p for p in promocoes
    }

    pratos_formatados = []

    for p in pratos:
        promocao = mapa_promocoes.get((p.id, p.unidade_id))

        if promocao and promocao.ativo:
            preco_final = p.preco * (1 - promocao.desconto / 100)
            promo = True
        else:
            preco_final = p.preco
            promo = False

        pratos_formatados.append({
            "id": p.id,
            "nome": p.nome,
            "preco_original": p.preco,
            "preco": round(preco_final, 2),
            "promocao": promo,
            "desconto": promocao.desconto if promocao else None,
            "unidade": p.unidade.nome if p.unidade else "-",
            "ativo": p.ativo
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

@router.get("/cardapio/editar/{id}")
def editar_cardapio(request: Request, id: int):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()

    prato = db.query(Prato).filter(Prato.id == id).first()
    unidades = db.query(Unidade).all()
    db.close()
    return templates.TemplateResponse(
        name="editar_cardapio.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "prato": prato,
            "erro": None,
            "unidades": unidades
        }
    )

@router.post("/cardapio/atualizar/{id}")
def atualizar_prato(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    unidade_id: int = Form(...),
    ativo: str = Form(None)):
    response = verificar_login(request)
    if response:
        return response

    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    prato = db.query(Prato).filter(
        Prato.id == id
    ).first()
    prato.nome = nome
    prato.descricao = descricao
    prato.preco = preco
    prato.unidade_id = unidade_id
    prato.ativo = True if ativo == "on" else False

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        unidades = db.query(Unidade).all()
        return templates.TemplateResponse(
            name="editar_cardapio.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "prato": prato,
                "unidades": unidades,
                "erro": "Houve algum erro."
            }
        )
    db.close()
    return RedirectResponse(
        "/cardapio",
        status_code=303
    )

@router.get("/cardapio/criar")
def novo_prato(request: Request):
    response = verificar_login(request)
    if response:
        return response

    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    unidades = db.query(Unidade).all()

    return templates.TemplateResponse(
        name="cardapio_form.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "unidades": unidades,
            "erro": None
        }
    )

@router.post("/cardapio/criar")
def criar_prato(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    unidade_id: int = Form(...)):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    novo = Prato(
        nome=nome,
        descricao=descricao,
        ativo=True,
        preco=preco,
        unidade_id=unidade_id
    )
    db.add(novo)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        unidades = db.query(Unidade).all()
        db.close()
        return templates.TemplateResponse(
            name="cardapio_form.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "unidades": unidades,
                "erro": "Erro ao cadastrar prato."
            }
        )
    db.close()
    return RedirectResponse( "/cardapio",status_code=303 )


@router.post("/cardapio/deletar/{id}")
def deletar_prato(request: Request, id: int):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    prato = db.query(Prato).filter(Prato.id == id).first()
    prato.ativo = False
    db.commit()
    db.close()

    return RedirectResponse("/cardapio", status_code=303)
