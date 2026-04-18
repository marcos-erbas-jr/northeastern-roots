from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse

def verificar_login(request: Request):
    if request.cookies.get("logado") != "true":
        return RedirectResponse(url="/login", status_code=302)

def verificar_role(request: Request, roles_permitidos: list):
    role = request.cookies.get("role")

    if role not in roles_permitidos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado"
        )