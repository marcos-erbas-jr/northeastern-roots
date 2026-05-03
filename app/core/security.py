from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

def gerar_hash(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash: str):
    return pwd_context.verify(senha, hash)

def verificar_login(request: Request):
    if request.cookies.get("logado") != "true":
        return RedirectResponse(url="/login", status_code=302)

def verificar_role(request: Request, roles_permitidos: list):
    role = request.cookies.get("role")

    if not role or role not in roles_permitidos:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso não autorizado"
        )

def get_usuario_atual(request: Request):
    if request.cookies.get("logado") != "true":
        raise HTTPException(status_code=401, detail="Não autenticado")

    return {
        "role": request.cookies.get("role")
    }

def verificar_permissao(request: Request, roles_permitidos: list):
    role = request.cookies.get("role")
    if role not in roles_permitidos:
        return RedirectResponse("/painel", status_code=302)