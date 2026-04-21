from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.security import verificar_login
from app.core.database import SessionLocal
from app.models.unidade import Unidade

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/unidades")
def pagina_unidades(request: Request):
    response = verificar_login(request)
    if response:
        return response

    db = SessionLocal()
    unidades = db.query(Unidade).all()
    db.close()

    return templates.TemplateResponse(
        name="unidades.html",
        request=request,
        context={
            "role": request.cookies.get("role"),
            "unidades": unidades
        }
    )