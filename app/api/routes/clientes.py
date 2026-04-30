from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login
from app.core.database import SessionLocal
from app.models.cliente import Cliente
from fastapi.responses import RedirectResponse

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

@router.post("/clientes/criar")
def criar_cliente(
        request: Request,
        nome: str = Form(...),
        email: str = Form(...),
        telefone: str = Form(None)):
        response = verificar_login(request)
        if response:
            return response

        db = SessionLocal()
        existe = db.query(Cliente).filter(Cliente.email == email).first()
        if existe:
            db.close()
            return RedirectResponse("/clientes", status_code=303)

        novo = Cliente(
            nome=nome,
            email=email,
            telefone=telefone
        )
        db.add(novo)
        db.commit()
        db.close()

        return RedirectResponse("/clientes", status_code=303)

@router.get("/registro_cliente")
def registro_cliente(request: Request):

    response = verificar_login(request)
    if response:
        return response

    return templates.TemplateResponse(
        name="registro_cliente.html",
        request=request,
        context={
            "role": request.cookies.get("role")
        }
    )

@router.get("/clientes/deletar/{cliente_id}")
def deletar_cliente(request: Request, cliente_id: int):
    response = verificar_login(request)
    if response:
        return response
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        if cliente.pedidos:
            db.close()
            return RedirectResponse("/clientes", status_code=303)

        db.delete(cliente)
        db.commit()

    db.close()
    return RedirectResponse("/clientes", status_code=303)

@router.get("/clientes/editar/{cliente_id}")
def editar_cliente(request: Request, cliente_id: int):
    response = verificar_login(request)
    if response:
        return response
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    db.close()
    return templates.TemplateResponse(
        name="editar_cliente.html",
        request=request,
        context={
            "cliente": cliente,
            "role": request.cookies.get("role")
        }
    )

@router.post("/clientes/atualizar/{cliente_id}")
def atualizar_cliente(
    request: Request,
    cliente_id: int,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(None)):
    response = verificar_login(request)
    if response:
        return response

    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

    if cliente:
        cliente.nome = nome
        cliente.email = email
        cliente.telefone = telefone
        db.commit()
    db.close()
    return RedirectResponse("/clientes", status_code=303)