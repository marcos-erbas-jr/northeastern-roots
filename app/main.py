from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import auth, home, painel, pedidos, promocao, unidades, estoque, cardapio, usuarios, clientes, restaurante
from app.core.database import Base, engine
from app.models import usuario, prato

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(painel.router)
app.include_router(pedidos.router)
app.include_router(cardapio.router)
app.include_router(estoque.router)
app.include_router(promocao.router)
app.include_router(unidades.router)
app.include_router(usuarios.router)
app.include_router(clientes.router)
app.include_router(restaurante.router)

