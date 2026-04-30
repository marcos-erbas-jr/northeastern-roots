from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.database import SessionLocal
from app.models.prato import Prato

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/restaurante")
def pagina_restaurante(request: Request, unidade_id: int):
    db = SessionLocal()
    pratos = db.query(Prato).filter(
        Prato.unidade_id == unidade_id
    ).all()
    db.close()
    return templates.TemplateResponse(
        name="restaurante.html",
        request=request,
        context={
            "pratos": pratos,
            "unidade_id": unidade_id
        }
    )