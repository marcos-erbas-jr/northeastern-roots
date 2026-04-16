from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def pagina_home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request
    )

