from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/clientes")
def pagina_clientes(request: Request):

    response = verificar_login(request)
    if response:
        return response

    return templates.TemplateResponse(
        name="clientes.html",
        request=request,
        context={
            "role": request.cookies.get("role")
        }
    )