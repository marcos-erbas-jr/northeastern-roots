from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.database import SessionLocal
from app.models.unidade import Unidade

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def index(request: Request):
    db = SessionLocal()
    unidades = db.query(Unidade).all()
    db.close()


    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={"unidades": unidades}
    )