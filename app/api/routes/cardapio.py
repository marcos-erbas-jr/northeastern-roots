from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/cardapio")
def pagina_cardapios(request: Request):

    response = verificar_login(request)
    if response:
        return response

    return templates.TemplateResponse(
        name="cardapio.html",
        request=request,
        context={
            "role": request.cookies.get("role")
        }
    )