import random
import uuid

def processar_pagamento_mock(valor):
    aprovado = random.choice([True, True, True, False])
    return {
        "status": "aprovado" if aprovado else "recusado",
        "transacao_id": str(uuid.uuid4()),
        "valor": valor
    }