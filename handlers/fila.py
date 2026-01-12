class Fila(Base):
    __tablename__ = "fila"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    produto = Column(String)
    criado_em = Column(DateTime)

from database import SessionLocal
from models import Fila
from datetime import datetime

async def adicionar_na_fila(user_id: int, produto: str):
    async with SessionLocal() as session:
        fila = Fila(
            telegram_id=user_id,
            produto=produto,
            criado_em=datetime.utcnow()
        )
        session.add(fila)
        await session.commit()
        from sqlalchemy.future import select
from models import Fila

async def pegar_primeiro_da_fila(produto: str):
    async with SessionLocal() as session:
        fila = await session.scalar(
            select(Fila)
            .where(Fila.produto == produto)
            .order_by(Fila.criado_em.asc())
        )
        return fila
from models import Estoque, Fila
from sqlalchemy.future import select

async def entregar_para_fila(bot, produto: str, conteudo: str, imagem: str):
    async with SessionLocal() as session:
        fila = await session.scalar(
            select(Fila)
            .where(Fila.produto == produto)
            .order_by(Fila.criado_em.asc())
        )

        if not fila:
            return False  # ninguém na fila

        # ENTREGA
        await bot.send_message(
            fila.telegram_id,
            f"📦 *SEU PRODUTO CHEGOU!*\n\n"
            f"🔐 `{conteudo}`",
            parse_mode="Markdown"
        )

        if imagem:
            await bot.send_photo(fila.telegram_id, imagem)

        # REMOVE DA FILA
        await session.delete(fila)
        await session.commit()

        return True

