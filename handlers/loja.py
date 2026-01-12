from aiogram import Router, types, F
from keyboards.loja import menu_loja

router = Router()

@router.callback_query(F.data == "loja")
async def abrir_loja(call: types.CallbackQuery):
    await call.message.answer(
        "🛒 *RC STORE — LOJA*\n\n"
        "Escolha um produto abaixo:",
        parse_mode="Markdown",
        reply_markup=menu_loja
    )
