from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse
from app.core.database import SessionLocal
from app.models.usuario import Usuario
from app.core.security import verificar_senha

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
'''
usuarios = {
    "admin@raizesdonordeste.com": {"senha": "12345678", "role": "admin"},
    "atendente@raizesdonordeste.com": {"senha": "12345678", "role": "atendente"},
    "cozinha@raizesdonordeste.com": {"senha": "12345678", "role": "cozinha"},
}

def autenticar_usuario(email, senha):
    usuario = usuarios.get(email)
    if usuario and usuario["senha"] == senha:
        return usuario
    return None
'''

@router.get("/login")
def pagina_login(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        request=request
    )

@router.post("/login")
def login(request: Request, email: str = Form(...), senha: str = Form(...)):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if usuario and verificar_senha(senha, usuario.senha):
        response = RedirectResponse(url="/painel", status_code=302)
        response.set_cookie("logado", "true")
        response.set_cookie("role", usuario.role)
        return response

    return templates.TemplateResponse(
        name="login.html",
        request=request,
        context={"erro": "Email ou senha inválidos"}
    )

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("logado")
    response.delete_cookie("role")
    return response