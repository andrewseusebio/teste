from fastapi import APIRouter, Request
from sqlalchemy.future import select
from database import SessionLocal
from models import User
from config import ASAAS_WEBHOOK_TOKEN

router = APIRouter()


@router.post("/webhook/asaas")
async def webhook_asaas(request: Request):
    data = await request.json()

    token = request.headers.get("asaas-token")
    if token != ASAAS_WEBHOOK_TOKEN:
        return {"error": "unauthorized"}

    if data.get("event") == "PAYMENT_RECEIVED":
        payment = data.get("payment", {})
        descricao = payment.get("description", "")
        valor = float(payment.get("value", 0))

        try:
            telegram_id = int(descricao.split()[-1])
        except Exception:
            return {"error": "invalid description"}

        async with SessionLocal() as session:
            user = await session.scalar(
                select(User).where(User.telegram_id == telegram_id)
            )

            if user:
                user.saldo += valor
                await session.commit()

    return {"status": "ok"}
