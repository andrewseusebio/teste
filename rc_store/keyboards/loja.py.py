from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_loja = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🎲 MIX PEDIDOS - R$125", callback_data="comprar_mix")],
    [InlineKeyboardButton(text="🥇💎 +10 PEDIDOS FÍSICOS - R$155", callback_data="comprar_fisico")],
    [InlineKeyboardButton(text="🍿🎥 PEDIDOS DIGITAIS - R$70", callback_data="comprar_digital")],
    [InlineKeyboardButton(text="🗂 RESERVA +10 PEDIDOS - R$200", callback_data="comprar_reserva")],
    [InlineKeyboardButton(text="⬅️ Voltar", callback_data="menu")]
])
