from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.routes import auth
from app.api.routes import home
from app.api.routes import painel

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(painel.router)

