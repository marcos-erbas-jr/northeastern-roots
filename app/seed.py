from app.core.database import SessionLocal
from app.core.database import Base, engine
from app.models.usuario import Usuario
from app.core.security import gerar_hash

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    usuarios = [
        {
            "nome": "Admin",
            "email": "admin@raizesdonordeste.com",
            "senha": "12345678",
            "role": "admin",
            "unidade_id": 1
        },
        {
            "nome": "Atendente",
            "email": "atendente@raizesdonordeste.com",
            "senha": "12345678",
            "role": "atendente",
            "unidade_id": 1
        },
        {
            "nome": "Cozinha",
            "email": "cozinha@raizesdonordeste.com",
            "senha": "123456",
            "role": "cozinha",
            "unidade_id": 1
        }
    ]
    for u in usuarios:
        existe = db.query(Usuario).filter(Usuario.email == u["email"]).first()
        if not existe:
            novo = Usuario(
                nome=u["nome"],
                email=u["email"],
                senha=gerar_hash(u["senha"]),
                role=u["role"],
                unidade_id=u["unidade_id"]
            )
            db.add(novo)

    db.commit()
    db.close()

    print("Seed executado")

if __name__ == "__main__":
    seed()