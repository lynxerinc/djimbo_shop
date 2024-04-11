# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from tgbot.database.db_payments import Paymentsx
from tgbot.keyboards.inline_admin import payment_method_finl, payment_yoomoney_finl, close_finl, payment_qiwi_finl
from tgbot.services.api_qiwi import QiwiAPI
from tgbot.services.api_yoomoney import YoomoneyAPI
from tgbot.utils.const_functions import ded
from tgbot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)


################################################################################
############################ CHOIX DU MODE DE RECHARGEMENT ######################
# Ouverture des modes de rechargement
@router.message(F.text == "🖲 Modes de rechargement")
async def payment_methods(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🖲 Choisissez les modes de rechargement</b>",
        reply_markup=payment_method_finl(),
    )


# Activation/désactivation des modes de rechargement
@router.callback_query(F.data.startswith("payment_method:"))
async def payment_methods_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    way_pay = call.data.split(":")[1]
    way_status = call.data.split(":")[2]

    get_payment = Paymentsx.get()

    if way_pay == "QIWI":
        if way_status == "True" and get_payment.qiwi_login == "None":
            return await call.answer("❗ Ajoutez un portefeuille QIWI avant d'activer les modes de rechargement", True)

        Paymentsx.update(way_qiwi=way_status)
    elif way_pay == "Yoomoney":
        if way_status == "True" and get_payment.yoomoney_token == "None":
            return await call.answer("❗ Ajoutez un portefeuille Yoomoney avant d'activer les modes de rechargement", True)

        Paymentsx.update(way_yoomoney=way_status)

    await call.message.edit_text(
        "<b>🖲 Choisissez les modes de rechargement</b>",
        reply_markup=payment_method_finl(),
    )


# Ouverture de Yoomoney
@router.message(F.text == "🔮 Yoomoney")
async def payment_yoomoney_open(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🔮 Gestion - Yoomoney</b>",
        reply_markup=payment_yoomoney_finl(),
    )


# Ouverture de QIWI
@router.message(F.text == "🥝 QIWI")
async def payment_qiwi_open(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🥝 Gestion - QIWI</b>",
        reply_markup=payment_qiwi_finl(),
    )


################################################################################
#################################### Yoomoney ##################################
# Solde Yoomoney
@router.callback_query(F.data == "payment_yoomoney_balance")
async def payment_yoomoney_balance(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    response = await YoomoneyAPI(
        bot=bot,
        arSession=arSession,
        update=call,
        skipping_error=True,
    ).balance()

    await call.message.answer(
        response,
        reply_markup=close_finl(),
    )


# Vérification Yoomoney
@router.callback_query(F.data == "payment_yoomoney_check")
async def payment_yoomoney_check(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    response = await YoomoneyAPI(
        bot=bot,
        arSession=arSession,
        update=call,
        skipping_error=True,
    ).check()

    await call.message.answer(
        response,
        reply_markup=close_finl(),
    )


# Modification Yoomoney
@router.callback_query(F.data == "payment_yoomoney_edit")
async def payment_yoomoney_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    response = await YoomoneyAPI(
        bot=bot,
        arSession=arSession
    ).authorization_get()

    await state.set_state("here_yoomoney_token")
    await call.message.edit_text(
        ded(f"""
            <b>🔮 Pour modifier le portefeuille Yoomoney</b>
            ▪️ Suivez le lien ci-dessous et autorisez l'application.
            ▪️ Après autorisation, envoyez le lien ou le code de la barre d'adresse.
            🔗 {response}
        """),
        disable_web_page_preview=True,
    )


################################ ACCEPTATION YOOMONEY ############################
# Acceptation du token Yoomoney
@router.message(StateFilter("here_yoomoney_token"))
async def payment_yoomoney_edit_token(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    cache_message = await message.answer("<b>🔮 Vérification des données Yoomoney saisies... 🔄</b>")

    get_code = message.text

    try:
        get_code = get_code[get_code.index("code=") + 5:].replace(" ", "")
    except:
        ...

    status, token, response = await YoomoneyAPI(
        bot=bot,
        arSession=arSession,
    ).authorization_enter(str(get_code))

    if status:
        Paymentsx.update(yoomoney_token=token)

    await cache_message.edit_text(response)

    await message.answer(
        "<b>🔮 Gestion - Yoomoney</b>",
        reply_markup=payment_yoomoney_finl(),
    )


################################################################################
##################################### QIWI #####################################
# Solde QIWI
@router.callback_query(F.data == "payment_qiwi_balance")
async def payment_qiwi_balance(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    response = await QiwiAPI(
        bot=bot,
        arSession=arSession,
        update=call,
        skipping_error=True,
    ).balance()

    await call.message.answer(
        response,
        reply_markup=close_finl(),
    )


# Vérification QIWI
@router.callback_query(F.data == "payment_qiwi_check")
async def payment_qiwi_check(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    status, response = await QiwiAPI(
        bot=bot,
        arSession=arSession,
        update=call,
    ).check()

    await call.message.answer(
        response,
        reply_markup=close_finl(),
    )


# Modification QIWI
@router.callback_query(F.data == "payment_qiwi_edit")
async def payment_qiwi_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.set_state("here_qiwi_login")
    await call.message.edit_text(
        "<b>🥝 Entrez le <code>numéro (avec +7, +380)</code> du portefeuille QIWI</b>"
    )


################################ ACCEPTATION QIWI ##############################
# Acceptation du login QIWI
@router.message(F.text, StateFilter("here_qiwi_login"))
async def payment_qiwi_edit_login(message: Message, bot: Bot, state: FSM, arSession: ARS):
    if message.text.startswith("+"):
        await state.update_data(here_qiwi_login=message.text)

        await state.set_state("here_qiwi_token")
        await message.answer(
            "<b>🥝 Entrez le <code>token API</code> du portefeuille QIWI 🖍</b>\n"
            "❕ Vous pouvez l'obtenir ici 👉 <a href='https://qiwi.com/api-info'><b>Cliquez sur moi</b></a>",
            disable_web_page_preview=True
        )
    else:
        await message.answer(
            "<b>❌ Le numéro doit commencer par + <code>(+7..., +380...)</code></b>\n"
            "🥝 Entrez le <code>numéro (avec +7, +380)</code> du portefeuille QIWI 🖍",
        )


# Acceptation du token QIWI
@router.message(F.text, StateFilter("here_qiwi_token"))
async def payment_qiwi_edit_token(message: Message, bot: Bot, state: FSM, arSession: ARS):
    qiwi_login = (await state.get_data())['here_qiwi_login']
    qiwi_token = message.text

    await state.clear()

    cache_message = await message.answer("<b>🥝 Vérification des données QIWI saisies... 🔄</b>")

    status, response = await QiwiAPI(
        bot=bot,
        arSession=arSession,
        login=qiwi_login,
        token=qiwi_token,
    ).edit()

    if status:
        Paymentsx.update(
            qiwi_login=qiwi_login,
            qiwi_token=qiwi_token,
        )

    await cache_message.edit_text(response)

    await message.answer(
        "<b>🥝 Gestion - QIWI</b>",
        reply_markup=payment_qiwi_finl(),
    )
