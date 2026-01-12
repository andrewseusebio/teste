from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from payments.asaas import criar_pix

router = Router()


class Deposito(StatesGroup):
    valor = State()


@router.callback_query(F.data == "saldo")
async def solicitar_valor(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        "💰 *Adicionar saldo*\n\n"
        "Digite o valor que deseja adicionar:",
        parse_mode="Markdown"
    )
    await state.set_state(Deposito.valor)


@router.message(Deposito.valor)
async def gerar_pix(msg: types.Message, state: FSMContext):
    try:
        valor = float(msg.text.replace(",", "."))
    except ValueError:
        await msg.answer("❌ Valor inválido. Digite apenas números.")
        return

    if valor <= 0:
        await msg.answer("❌ O valor deve ser maior que zero.")
        return

    pix = criar_pix(valor, f"Saldo {msg.from_user.id}")

    payload = pix["pixTransaction"]["payload"]
    qr_base64 = pix["pixTransaction"]["encodedImage"]

    await msg.answer(
        f"💳 *PIX GERADO*\n\n"
        f"💰 Valor: R$ {valor:.2f}\n\n"
        f"📋 *PIX Copia e Cola:*\n"
        f"`{payload}`\n\n"
        f"⏳ Após o pagamento o saldo será creditado automaticamente.",
        parse_mode="Markdown"
    )

    await msg.answer_photo(
        photo=f"data:image/png;base64,{qr_base64}",
        caption="📸 Escaneie o QR Code para pagar"
    )

    await state.clear()
