from aiogram import Router, types, F
from sqlalchemy.future import select
from database import SessionLocal
from models import User
from produtos import PRODUTOS  # ou cole o dict direto aqui

router = Router()

async def processar_compra(call: types.CallbackQuery, produto_key: str):
    async with SessionLocal() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == call.from_user.id)
        )

        # Usuário não existe → cria
        if not user:
            user = User(
                telegram_id=call.from_user.id,
                username=call.from_user.username
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

        # BANIDO
        if user.banido:
            await call.message.answer("⛔ Você está banido.")
            return

        produto = PRODUTOS[produto_key]
        preco = produto["preco"]

        # SALDO INSUFICIENTE
        if user.saldo < preco:
            await call.message.answer(
                f"❌ Saldo insuficiente.\n\n"
                f"💰 Preço: R${preco}\n"
                f"💳 Seu saldo: R${user.saldo:.2f}"
            )
            return

        # DESCONTA SALDO
        user.saldo -= preco
        await session.commit()

        # CONFIRMAÇÃO
        await call.message.answer(
            f"✅ *Compra realizada com sucesso!*\n\n"
            f"📦 Produto: {produto['nome']}\n"
            f"💰 Valor: R${preco}\n"
            f"💳 Saldo restante: R${user.saldo:.2f}",
            parse_mode="Markdown"
        )

        # AQUI VAI:
        # - entrega automática
        # - OU fila (reserva)

@router.callback_query(F.data == "comprar_mix")
async def comprar_mix(call: types.CallbackQuery):
    await processar_compra(call, "mix")

@router.callback_query(F.data == "comprar_fisico")
async def comprar_fisico(call: types.CallbackQuery):
    await processar_compra(call, "fisico")

@router.callback_query(F.data == "comprar_digital")
async def comprar_digital(call: types.CallbackQuery):
    await processar_compra(call, "digital")

@router.callback_query(F.data == "comprar_reserva")
async def comprar_reserva(call: types.CallbackQuery):
    await processar_compra(call, "reserva")

            # 🔹 SE FOR RESERVA → SEMPRE FILA
        if produto_key == "reserva":
            await adicionar_na_fila(call.from_user.id, "fisico")
            await call.message.answer(
                "🗂 *RESERVA CONFIRMADA*\n\n"
                "📌 Você entrou na fila do +10 PEDIDOS FÍSICOS.\n"
                "🔔 A entrega será automática quando houver reposição.",
                parse_mode="Markdown"
            )
            return

        # 🔹 TENTA ENTREGAR (SE NÃO TIVER ESTOQUE → FILA AUTOMÁTICA)
        entregue = await entregar_produto(
            call.bot,
            call.from_user.id,
            produto_key
        )

        if entregue:
            await call.message.answer(
                "✅ Produto entregue com sucesso!\n"
                "📦 Confira a mensagem acima."
            )

    
