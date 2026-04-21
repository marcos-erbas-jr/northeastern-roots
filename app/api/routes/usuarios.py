from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.models.unidade import Unidade

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/usuarios")
def pagina_usuarios(request: Request, unidade_id: int = None):

    response = verificar_login(request)
    if response:
        return response

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