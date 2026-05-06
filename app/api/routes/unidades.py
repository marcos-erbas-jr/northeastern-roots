from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login, verificar_permissao
from app.core.database import SessionLocal
from app.models.unidade import Unidade
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import IntegrityError

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/unidades")
def pagina_unidades(request: Request):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm

    db = SessionLocal()
    unidades = db.query(Unidade).all()
    db.close()

    return templates.TemplateResponse(
        name="unidades.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "unidades": unidades
        }
    )

@router.get("/unidades/nova")
def nova_unidade(request: Request):
    response = verificar_login(request)
    if response:
        return response

    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm

    return templates.TemplateResponse(
        name="unidade_form.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "unidade": None,
            "erro": None
        }
    )

@router.post("/unidades/criar")
def criar_unidade(request: Request,
    nome: str = Form(...),
    cidade: str = Form(...)):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    nova = Unidade(
        nome=nome,
        cidade=cidade,
        ativo=True
    )

    db.add(nova)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        db.close()
        return templates.TemplateResponse(
            name="unidade_form.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "unidade": None,
                "erro": "já existe uma unidade com esse nome"
            }
        )



    db.close()
    return RedirectResponse("/unidades", status_code=303)

@router.get("/unidades/editar/{id}")
def editar_unidade(request: Request, id: int):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    unidade = db.query(Unidade).filter(Unidade.id == id).first()
    db.close()
    return templates.TemplateResponse(
            name="editar_unidade.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "unidade": unidade,
                "erro": None
            }
        )


@router.post("/unidades/atualizar/{id}")
def atualizar_unidade(request: Request,
    id: int,
    nome: str = Form(...),
    cidade: str = Form(...),ativo: str = Form(None)):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    unidade = db.query(Unidade).filter(Unidade.id == id).first()
    unidade.nome = nome
    unidade.cidade = cidade
    unidade.ativo = True if ativo == "on" else False

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        return templates.TemplateResponse(
            name="unidade_form.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "unidade": None,
                "erro": "Nome já utilizado"
            }
        )

    db.close()
    return RedirectResponse("/unidades", status_code=303)

@router.post("/unidades/deletar/{id}")
def deletar_unidade(request: Request, id: int):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    unidade = db.query(Unidade).filter(Unidade.id == id).first()
    unidade.ativo = False
    db.commit()
    db.close()

    return RedirectResponse("/unidades", status_code=303)