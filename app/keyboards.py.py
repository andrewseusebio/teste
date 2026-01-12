from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🛒 Loja", callback_data="loja")],
    [InlineKeyboardButton(text="💰 Saldo", callback_data="saldo")],
    [
        InlineKeyboardButton(text="📦 Meus pedidos", callback_data="pedidos"),
        InlineKeyboardButton(text="👤 Perfil", callback_data="perfil")
    ],
    [InlineKeyboardButton(text="🆘 Suporte", callback_data="suporte")]
])

PRODUTOS = {
    "mix": {"nome": "🎲 MIX PEDIDOS", "preco": 125},
    "fisico": {"nome": "🥇💎 +10 PEDIDOS FÍSICOS", "preco": 155},
    "digital": {"nome": "🍿🎥 PEDIDOS DIGITAIS", "preco": 70},
    "reserva": {"nome": "🗂 RESERVA +10 PEDIDOS FÍSICOS", "preco": 200},
}
