from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login, verificar_permissao
from app.core.database import SessionLocal
from app.models.estoque import Estoque
from app.models.unidade import Unidade
from app.models.prato import Prato
from app.models.ingrediente import Ingrediente
from app.models.estoque import Estoque
from app.models.receita import Receita
from fastapi.responses import RedirectResponse

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
    perm = verificar_permissao(request, ["admin", "cozinha"])
    if perm:
        return perm


    db = SessionLocal()
    unidades = db.query(Unidade).all()

    role = request.cookies.get("role")
    unidade_usuario = request.cookies.get("unidade_id")

    if role == "admin":
        if unidade_id:
            estoques = db.query(Estoque).filter(
                Estoque.unidade_id == unidade_id
            ).all()
        else:
            estoques = db.query(Estoque).all()
    else:
        estoques = db.query(Estoque).filter(
            Estoque.unidade_id == int(unidade_usuario)
        ).all()

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


@router.get("/estoque/novo")
def novo_estoque(request: Request):

    response = verificar_login(request)
    if response:
        return response

    perm = verificar_permissao(request, ["admin", "cozinha"])
    if perm:
        return perm

    db = SessionLocal()

    unidades = db.query(Unidade).all()
    pratos = db.query(Prato).all()

    ingredientes = db.query(Ingrediente).filter(
        Ingrediente.ativo == True
    ).all()

    db.close()

    return templates.TemplateResponse(
        name="estoque_form.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "unidades": unidades,
            "pratos": pratos,
            "ingredientes": ingredientes,
            "erro": None
        }
    )


@router.post("/estoque/criar")
def criar_estoque(
    request: Request,
    unidade_id: int = Form(...),
    quantidade: float = Form(...),
    prato_id: int = Form(None),
    novo_prato: str = Form(None),
    ingrediente_id: int = Form(None),
    novo_ingrediente: str = Form(None)):

    response = verificar_login(request)
    if response:
        return response

    perm = verificar_permissao(request, ["admin", "cozinha"])
    if perm:
        return perm

    db = SessionLocal()

    try:
        if novo_prato and novo_prato.strip() != "":

            prato = Prato(
                nome=novo_prato,
                descricao="Novo prato",
                preco=0,
                ativo=True,
                unidade_id=unidade_id
            )

            db.add(prato)
            db.flush()

        else:

            prato = db.query(Prato).filter(
                Prato.id == prato_id
            ).first()

        if novo_ingrediente and novo_ingrediente.strip() != "":

            ingrediente = Ingrediente(
                nome=novo_ingrediente,
                ativo=True,
                unidade_id=unidade_id
            )

            db.add(ingrediente)
            db.flush()

        else:

            ingrediente = db.query(Ingrediente).filter(
                Ingrediente.id == ingrediente_id
            ).first()

        receita_existente = db.query(Receita).filter(
            Receita.prato_id == prato.id,
            Receita.ingrediente_id == ingrediente.id).first()

        if not receita_existente:

            receita = Receita(
                prato_id=prato.id,
                ingrediente_id=ingrediente.id,
                quantidade=quantidade
            )

            db.add(receita)

        estoque_existente = db.query(Estoque).filter(
            Estoque.unidade_id == unidade_id,
            Estoque.ingrediente_id == ingrediente.id
        ).first()

        if estoque_existente:
            estoque_existente.quantidade += quantidade

        else:

            novo_estoque = Estoque(
                unidade_id=unidade_id,
                ingrediente_id=ingrediente.id,
                quantidade=quantidade
            )

            db.add(novo_estoque)
        db.commit()

    except Exception:

        db.rollback()
        unidades = db.query(Unidade).all()
        pratos = db.query(Prato).all()

        ingredientes = db.query(Ingrediente).filter(
            Ingrediente.ativo == True
        ).all()
        db.close()

        return templates.TemplateResponse(
            name="estoque_form.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "unidades": unidades,
                "pratos": pratos,
                "ingredientes": ingredientes,
                "erro": "Erro ao cadastrar item"
            }
        )

    db.close()
    return RedirectResponse(
        "/estoque",
        status_code=303
    )

@router.get("/estoque/editar/{id}")
def editar_estoque(request: Request, id: int):

    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin", "cozinha"])
    if perm:
        return perm

    db = SessionLocal()
    estoque = db.query(Estoque).filter(
        Estoque.id == id
    ).first()
    unidades = db.query(Unidade).all()
    ingredientes = db.query(Ingrediente).filter(
        Ingrediente.ativo == True
    ).all()

    db.close()

    return templates.TemplateResponse(
        name="editar_estoque.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "estoque": estoque,
            "unidades": unidades,
            "ingredientes": ingredientes,
            "erro": None
        }
    )


@router.post("/estoque/atualizar/{id}")
def atualizar_estoque(
    request: Request,
    id: int,
    unidade_id: int = Form(...),
    ingrediente_id: int = Form(...),
    quantidade: float = Form(...)):

    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin", "cozinha"])
    if perm:
        return perm

    db = SessionLocal()

    estoque = db.query(Estoque).filter(
        Estoque.id == id
    ).first()
    estoque.unidade_id = unidade_id
    estoque.ingrediente_id = ingrediente_id
    estoque.quantidade = quantidade

    try:

        db.commit()

    except Exception:

        db.rollback()
        unidades = db.query(Unidade).all()
        ingredientes = db.query(Ingrediente).filter(
            Ingrediente.ativo == True
        ).all()
        return templates.TemplateResponse(
            name="editar_estoque.html",
            request=request,
            context={
                "role": request.cookies.get("role"),
                "estoque": estoque,
                "unidades": unidades,
                "ingredientes": ingredientes,
                "erro": "Erro ao atualizar item"
            }
        )

    db.close()
    return RedirectResponse(
        "/estoque",
        status_code=303
    )

@router.get("/estoque/excluir/{id}")
def excluir_estoque(request: Request, id: int):
    response = verificar_login(request)
    if response:
        return response
    perm = verificar_permissao(request, ["admin", "cozinha"])
    if perm:
        return perm
    db = SessionLocal()

    estoque = db.query(Estoque).filter(
        Estoque.id == id
    ).first()
    if estoque:
        db.delete(estoque)
        db.commit()
    db.close()
    return RedirectResponse(
        "/estoque",
        status_code=303
    )