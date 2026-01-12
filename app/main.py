import asyncio
from fastapi import FastAPI
from bot import bot, dp
from payments.webhook import router as webhook_router
from handlers import start, loja, compra, saldo, admin, estoque, fila, suporte

app = FastAPI()
app.include_router(webhook_router)

@app.on_event("startup")
async def startup():
    dp.include_routers(
        start.router,
        loja.router,
        compra.router,
        saldo.router,
        admin.router,
        estoque.router,
        fila.router,
        suporte.router
    )
    asyncio.create_task(dp.start_polling(bot))
