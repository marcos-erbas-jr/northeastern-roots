from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/painel")
def pagina_painel(request: Request):
    if request.cookies.get("logado") != "true":
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        name="painel.html",
        request=request
    )