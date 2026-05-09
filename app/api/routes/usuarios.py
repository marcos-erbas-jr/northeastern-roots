from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login, verificar_permissao
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.models.unidade import Unidade
from sqlalchemy.exc import IntegrityError
from fastapi.responses import RedirectResponse
from app.core.security import gerar_hash

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/usuarios")
def pagina_usuarios(request: Request, unidade_id: int = None):

    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm

    db = SessionLocal()
    unidades = db.query(Unidade).all()
    if unidade_id:
        usuarios = db.query(Usuario).filter(Usuario.unidade_id == unidade_id).all()
    else:
        usuarios = db.query(Usuario).all()
    usuarios_formatados = []
    for u in usuarios:
        usuarios_formatados.append({
            "id": u.id,
            "nome": u.nome,
            "role": u.role,
            "unidade": u.unidade.nome if u.unidade else "-"
        })
    db.close()

    return templates.TemplateResponse(
        name="usuarios.html",
        request=request,
        context={
            "usuarios": usuarios_formatados,
            "unidades": unidades,
            "role": request.cookies.get("role")
        }
    )

@router.get("/usuarios/novo")
def novo_usuario(request: Request):

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
        name="novo_usuario.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "unidades": unidades,
            "erro": None
        }
    )

@router.post("/usuarios/criar")
def criar_usuario(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    role: str = Form(...),
    unidade_id: int = Form(...)):

    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()

    novo = Usuario(
        nome=nome,
        email=email,
        senha=gerar_hash(senha),
        role=role,
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
            name="novo_usuario.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "unidades": unidades,
                "erro": "Email já cadastrado."
            }
        )
    db.close()
    return RedirectResponse(
        "/usuarios",
        status_code=303
    )

@router.get("/usuarios/editar/{id}")
def editar_usuario(request: Request, id: int):

    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm
    db = SessionLocal()
    usuario = db.query(Usuario).filter(
        Usuario.id == id
    ).first()
    unidades = db.query(Unidade).all()
    db.close()

    return templates.TemplateResponse(
        name="editar_usuario.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "usuario": usuario,
            "unidades": unidades,
            "erro": None
        }
    )


@router.post("/usuarios/atualizar/{id}")
def atualizar_usuario(
    request: Request,
    id: int,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(""),
    role: str = Form(...),
    unidade_id: int = Form(...)):

    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm

    db = SessionLocal()
    usuario = db.query(Usuario).filter(
        Usuario.id == id
    ).first()

    usuario.nome = nome
    usuario.email = email
    usuario.role = role
    usuario.unidade_id = unidade_id
    if senha:
        usuario.senha = gerar_hash(senha)

    try:
        db.commit()
    except IntegrityError:

        db.rollback()
        unidades = db.query(Unidade).all()

        return templates.TemplateResponse(
            name="editar_usuario.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "usuario": usuario,
                "unidades": unidades,
                "erro": "Email já cadastrado."
            }
        )
    db.close()
    return RedirectResponse(
        "/usuarios",
        status_code=303
    )

@router.get("/usuarios/excluir/{id}")
def excluir_usuario(request: Request, id: int):

    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin"])
    if perm:
        return perm

    db = SessionLocal()
    usuario = db.query(Usuario).filter(
        Usuario.id == id
    ).first()

    if usuario:
        db.delete(usuario)
        db.commit()
    db.close()
    return RedirectResponse(
        "/usuarios",
        status_code=303
    )