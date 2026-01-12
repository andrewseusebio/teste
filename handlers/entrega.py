from sqlalchemy.future import select
from database import SessionLocal
from models import Estoque
from handlers.fila import adicionar_na_fila

async def entregar_produto(bot, user_id: int, produto_key: str):
    async with SessionLocal() as session:
        item = await session.scalar(
            select(Estoque).where(Estoque.produto == produto_key)
        )

        # NÃO TEM ESTOQUE → ENTRA NA FILA
        if not item:
            await adicionar_na_fila(user_id, produto_key)
            await bot.send_message(
                user_id,
                "⏳ Produto esgotado.\n"
                "📌 Você entrou na fila automaticamente.\n"
                "🔔 A entrega será automática na reposição."
            )
            return False

        # ENTREGA NORMAL
        await bot.send_message(
            user_id,
            f"📦 *SEU PRODUTO*\n\n"
            f"🔐 `{item.conteudo}`",
            parse_mode="Markdown"
        )

        if item.imagem:
            await bot.send_photo(user_id, item.imagem)

        await session.delete(item)
        await session.commit()

        return True
