from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
def pagina_login(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        request=request
    )

@router.post("/login")
def login(email: str = Form(...), senha: str = Form(...)):

    if email == "admin@raizesdonordeste.com" and senha == "12345678":
        return RedirectResponse(url="/", status_code=302)

    return {"erro": "Login inválido"}