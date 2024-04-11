# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from tgbot.database.db_settings import Settingsx
from tgbot.database.db_users import Userx
from tgbot.keyboards.inline_admin import turn_open_finl, settings_open_finl
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import send_admins, insert_tags

router = Router(name=__name__)


# Modification des données
@router.message(F.text == "🖍 Modifier les données")
async def settings_data_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🖍 Modification des données du bot.</b>",
        reply_markup=settings_open_finl(),
    )


# Interrupteurs du bot
@router.message(F.text == "🕹 Interrupteurs")
async def settings_turn_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🕹 Activation et désactivation des fonctions principales</b>",
        reply_markup=turn_open_finl(),
    )


################################## INTERRUPTEURS #################################
# Activer/désactiver les travaux techniques
@router.callback_query(F.data.startswith("turn_work:"))
async def settings_turn_work(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_status = call.data.split(":")[1]

    get_user = Userx.get(user_id=call.from_user.id)
    Settingsx.update(status_work=get_status)

    if get_status == "True":
        send_text = "🔴 Mis le bot en maintenance."
    else:
        send_text = "🟢 Sorti le bot de maintenance."

    await send_admins(
        bot,
        f"👤 Administrateur <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>\n"
        f"{send_text}",
        not_me=get_user.user_id,
    )

    await call.message.edit_reply_markup(reply_markup=turn_open_finl())


# Activer/désactiver les achats
@router.callback_query(F.data.startswith("turn_buy:"))
async def settings_turn_buy(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_status = call.data.split(":")[1]

    get_user = Userx.get(user_id=call.from_user.id)
    Settingsx.update(status_buy=get_status)

    if get_status == "True":
        send_text = "🟢 Activé les achats dans le bot."
    else:
        send_text = "🔴 Désactivé les achats dans le bot."

    await send_admins(
        bot,
        f"👤 Administrateur <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>\n"
        f"{send_text}",
        not_me=get_user.user_id,
    )

    await call.message.edit_reply_markup(reply_markup=turn_open_finl())


# Activer/désactiver les recharges
@router.callback_query(F.data.startswith("turn_pay:"))
async def settings_turn_pay(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_status = call.data.split(":")[1]

    get_user = Userx.get(user_id=call.from_user.id)
    Settingsx.update(status_refill=get_status)

    if get_status == "True":
        send_text = "🟢 Activé les recharges dans le bot."
    else:
        send_text = "🔴 Désactivé les recharges dans le bot."

    await send_admins(
        bot,
        f"👤 Administrateur <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>\n"
        f"{send_text}",
        not_me=get_user.user_id,
    )

    await call.message.edit_reply_markup(reply_markup=turn_open_finl())


############################### MODIFICATION DES DONNÉES ###############################
# Modification du support
@router.callback_query(F.data == "settings_edit_support")
async def settings_support_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await state.set_state("here_settings_support")
    await call.message.edit_text(
        "<b>☎️ Envoyez le nom d'utilisateur pour le support.</b>\n"
        "❕ Nom d'utilisateur du utilisateur/bot/canal/chat.",
    )


# Modification de la FAQ
@router.callback_query(F.data == "settings_edit_faq")
async def settings_faq_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await state.set_state("here_settings_faq")
    await call.message.edit_text(
        "<b>❔ Entrez le nouveau texte pour la FAQ</b>\n"
        "❕ Vous pouvez utiliser la syntaxe prédéfinie et le formatage HTML :\n"
        "▶️ <code>{username}</code>  - nom d'utilisateur\n"
        "▶️ <code>{user_id}</code>   - ID de l'utilisateur\n"
        "▶️ <code>{firstname}</code> - prénom de l'utilisateur",
    )


# Modification de l'affichage des positions cachées
@router.callback_query(F.data.startswith("settings_edit_item_hide:"))
async def settings_item_hide_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    status = call.data.split(":")[1]

    Settingsx.update(misc_item_hide=status)

    await call.message.edit_text(
        "<b>🖍 Modification des données du bot.</b>",
        reply_markup=settings_open_finl(),
    )


################################ RÉCEPTION DES DONNÉES ###############################
# Réception du support
@router.message(F.text, StateFilter("here_settings_support"))
async def settings_support_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    get_support = message.text

    if get_support.startswith("@"):
        get_support = get_support[1:]

    await state.clear()

    Settingsx.update(misc_support=get_support)

    await message.answer(
        "<b>🖍 Modification des données du bot.</b>",
        reply_markup=settings_open_finl(),
    )


# Réception de la FAQ
@router.message(F.text, StateFilter("here_settings_faq"))
async def settings_faq_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    get_message = insert_tags(message.from_user.id, message.text)

    try:
        await (await message.answer(get_message)).delete()
    except:
        return await message.answer(
            "<b>❌ Erreur de syntaxe HTML.</b>\n"
            "❔ Entrez le nouveau texte pour la FAQ",
        )

    await state.clear()
    Settingsx.update(misc_faq=message.text)

    await message.answer(
        "<b>🖍 Modification des données du bot.</b>",
        reply_markup=settings_open_finl(),
    )
