# - *- coding: utf- 8 - *-
import asyncio

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from tgbot.database.db_purchases import Purchasesx
from tgbot.database.db_refill import Refillx
from tgbot.database.db_users import Userx
from tgbot.keyboards.inline_admin import profile_search_return_finl, mail_confirm_finl
from tgbot.utils.const_functions import is_number, to_number, del_message, ded, get_unix, clear_html, convert_date
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import upload_text
from tgbot.utils.text_functions import open_profile_admin, refill_open_admin, purchase_open_admin

router = Router(name=__name__)

# Recherche de reçus et de profils
@router.message(F.text == "🔍 Recherche")
async def functions_search(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    await state.set_state("here_search")
    await message.answer("<b>🔍 Envoyez l'ID/login de l'utilisateur ou le numéro du reçu</b>")

# Distribution
@router.message(F.text == "📢 Mailing")
async def functions_mail(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()
    await state.set_state("here_mail_text")
    await message.answer(
        "<b>📢 Entrez le texte pour la distribution aux utilisateurs</b>\n"
        "❕ Vous pouvez utiliser du HTML",
    )

##################################### RECHERCHE ####################################
# Acceptation de l'ID/login de l'utilisateur ou du reçu pour la recherche
@router.message(F.text, StateFilter("here_search"))
@router.message(F.text.lower().startswith(('.find', 'find')))
async def functions_search_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    find_data = message.text.lower()

    if ".find" in find_data or "find" in find_data:
        if len(find_data.split(" ")) >= 2:
            if ".find" in find_data or "find" in find_data:
                find_data = message.text.split(" ")[1]
        else:
            return await message.answer(
                "<b>❌ Vous n'avez pas fourni de données de recherche.</b>\n"
                "🔍 Envoyez l'ID/login de l'utilisateur ou le numéro du reçu",
            )

    if find_data.startswith("@") or find_data.startswith("#"):
        find_data = find_data[1:]

    if find_data.isdigit():
        get_user = Userx.get(user_id=find_data)
    else:
        get_user = Userx.get(user_login=find_data.lower())

    get_refill = Refillx.get(refill_receipt=find_data)
    get_purchase = Purchasesx.get(purchase_receipt=find_data)

    if get_user is None and get_refill is None and get_purchase is None:
        return await message.answer(
            "<b>❌ Aucune donnée trouvée</b>\n"
            "🔍 Envoyez l'ID/login de l'utilisateur ou le numéro du reçu",
        )

    await state.clear()

    if get_user is not None:
        return await open_profile_admin(bot, message.from_user.id, get_user)

    if get_refill is not None:
        return await refill_open_admin(bot, message.from_user.id, get_refill)

    if get_purchase is not None:
        return await purchase_open_admin(bot, arSession, message.from_user.id, get_purchase)

################################### DISTRIBUTION ###################################
# Acceptation du texte pour la distribution
@router.message(F.text, StateFilter("here_mail_text"))
async def functions_mail_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.update_data(here_mail_text="📢 Distribution.\n" + str(message.text))

    get_users = Userx.get_all()

    try:
        await (await message.answer(message.text)).delete()
    except:
        return await message.answer(
            "<b>❌ Erreur de syntaxe HTML.</b>\n"
            "📢 Entrez le texte pour la distribution aux utilisateurs.\n"
            "❕ Vous pouvez utiliser du HTML.",
        )

    await state.set_state("here_mail_confirm")

    await message.answer(
        f"<b>📢 Envoyer le message à <code>{len(get_users)}</code> utilisateurs ?</b>\n"
        f"{message.text}",
        reply_markup=mail_confirm_finl(),
        disable_web_page_preview=True
    )

# Confirmation de l'envoi de la distribution
@router.callback_query(F.data.startswith("confirm_mail:"), StateFilter("here_mail_confirm"))
async def functions_mail_confirm(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_action = call.data.split(":")[1]

    get_users = Userx.get_all()

    send_message = (await state.get_data())['here_mail_text']
    await state.clear()

    if get_action == "yes":
        await call.message.edit_text(f"<b>📢 La distribution commence... (0/{len(get_users)})</b>")

        await asyncio.create_task(functions_mail_make(bot, send_message, call))
    else:
        await call.message.edit_text("<b>📢 Vous avez annulé l'envoi de la distribution ✅</b>")

# L'envoi de la distribution
async def functions_mail_make(bot: Bot, text: str, call: CallbackQuery):
    users_receive, users_block, users_count = 0, 0, 0

    get_users = Userx.get_all()
    get_time = get_unix()

    for user in get_users:
        try:
            await bot.send_message(user.user_id, text)
            users_receive += 1
        except:
            users_block += 1

        users_count += 1

        if users_count % 10 == 0:
            await call.message.edit_text(f"<b>📢 La distribution commence... ({users_count}/{len(get_users)})</b>")

        await asyncio.sleep(0.07)

    await call.message.edit_text(
        ded(f"""
            <b>📢 La distribution est terminée en <code>{get_unix() - get_time}sec</code></b>
            ➖➖➖➖➖➖➖➖➖➖
            👤 Total d'utilisateurs: <code>{len(get_users)}</code>
            ✅ Utilisateurs ayant reçu le message: <code>{users_receive}</code>
            ❌ Utilisateurs n'ayant pas reçu le message: <code>{users_block}</code>
        """)
    )

############################## GESTION DU PROFIL #############################
# Mise à jour du profil utilisateur
@router.callback_query(F.data.startswith("admin_user_refresh:"))
async def functions_profile_refresh(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    user_id = call.data.split(":")[1]

    get_user = Userx.get(user_id=user_id)

    await state.clear()

    await del_message(call.message)
    await open_profile_admin(bot, call.from_user.id, get_user)


# Achats de l'utilisateur
@router.callback_query(F.data.startswith("admin_user_purchases:"))
async def functions_profile_purchases(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    user_id = call.data.split(":")[1]

    get_user = Userx.get(user_id=user_id)
    get_purchases = Purchasesx.gets(user_id=call.from_user.id)
    get_purchases = get_purchases[-10:]

    if len(get_purchases) < 1:
        return await call.answer("❗ L'utilisateur n'a aucun achat", True)

    await call.answer("🎁 Les 10 derniers achats")
    await del_message(call.message)

    for purchase in get_purchases:
        link_items = await upload_text(arSession, purchase.purchase_data)

        await call.message.answer(
            ded(f"""
                <b>🧾 Ticket: <code>#{purchase.purchase_receipt}</code></b>
                🎁 Article: <code>{purchase.purchase_position_name} | {purchase.purchase_count}pcs | {purchase.purchase_price}₽</code>
                🕰 Date d'achat: <code>{convert_date(purchase.purchase_unix)}</code>
                🔗 Articles: <a href='{link_items}'>cliquable</a>
            """)
        )

        await asyncio.sleep(0.2)

    await open_profile_admin(bot, call.from_user.id, get_user)


# Attribution de solde à l'utilisateur
@router.callback_query(F.data.startswith("admin_user_balance_add:"))
async def functions_profile_balance_add(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    user_id = call.data.split(":")[1]

    await state.update_data(here_profile=user_id)
    await state.set_state("here_profile_add")

    await call.message.edit_text(
        "<b>💰 Entrez le montant à créditer</b>",
        reply_markup=profile_search_return_finl(user_id),
    )


# Réception du montant pour créditer le solde de l'utilisateur
@router.message(F.text, StateFilter("here_profile_add"))
async def functions_profile_balance_add_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    user_id = (await state.get_data())['here_profile']

    if not is_number(message.text):
        return await message.answer(
            "<b>❌ Les données saisies sont incorrectes.</b>\n"
            "💰 Entrez le montant à créditer",
            reply_markup=profile_search_return_finl(user_id),
        )

    if to_number(message.text) <= 0 or to_number(message.text) > 1_000_000_000:
        return await message.answer(
            "<b>❌ Le montant à créditer ne peut être inférieur à 1 et supérieur à 1 000 000 000</b>\n"
            "💰 Entrez le montant à créditer",
            reply_markup=profile_search_return_finl(user_id),
        )

    await state.clear()

    get_user = Userx.get(user_id=user_id)
    Userx.update(
        user_id,
        user_balance=round(get_user.user_balance + to_number(message.text), 2),
        user_give=round(get_user.user_give + to_number(message.text), 2),
    )

    try:
        await bot.send_message(
            user_id,
            f"<b>💰 Vous avez été crédité de <code>{message.text}₽</code></b>",
        )
    except:
        ...

    await message.answer(
        f"👤 Utilisateur: <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>\n"
        f"💰 Solde crédité de <code>{message.text}₽</code>"
    )

    get_user = Userx.get(user_id=user_id)
    await open_profile_admin(bot, message.from_user.id, get_user)

# Modification du solde de l'utilisateur
@router.callback_query(F.data.startswith("admin_user_balance_set:"))
async def functions_profile_balance_set(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    user_id = call.data.split(":")[1]

    await state.update_data(here_profile=user_id)
    await state.set_state("here_profile_set")

    await call.message.edit_text(
        "<b>💰 Entrez le montant pour modifier le solde</b>",
        reply_markup=profile_search_return_finl(user_id),
    )


# Réception du montant pour la modification du solde de l'utilisateur
@router.message(F.text, StateFilter("here_profile_set"))
async def functions_profile_balance_set_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    user_id = (await state.get_data())['here_profile']

    if not is_number(message.text):
        return await message.answer(
            "<b>❌ Les données ont été saisies incorrectement.</b>\n"
            "💰 Entrez le montant pour modifier le solde",
            reply_markup=profile_search_return_finl(user_id),
        )

    if to_number(message.text) < -1_000_000_000 or to_number(message.text) > 1_000_000_000:
        return await message.answer(
            "<b>❌ Le montant de modification ne peut être supérieur ou inférieur à (-)1 000 000 000</b>\n"
            "💰 Entrez le montant pour modifier le solde",
            reply_markup=profile_search_return_finl(user_id),
        )

    await state.clear()

    get_user = Userx.get(user_id=user_id)

    if to_number(message.text) > get_user.user_balance:
        user_give = get_user.user_give + to_number(message.text)
    else:
        user_give = get_user.user_give

    Userx.update(
        user_id,
        user_balance=to_number(message.text),
        user_give=user_give,
    )

    await message.answer(
        f"👤 Utilisateur: <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>\n"
        f"💰 Solde modifié de <code>{message.text}₽</code>"
    )

    get_user = Userx.get(user_id=user_id)
    await open_profile_admin(bot, message.from_user.id, get_user)


# Envoi d'un message à l'utilisateur
@router.callback_query(F.data.startswith("admin_user_message:"))
async def functions_profile_user_message(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    user_id = call.data.split(":")[1]

    await state.update_data(here_profile=user_id)
    await state.set_state("here_profile_message")

    await call.message.edit_text(
        "<b>💌 Tapez le message à envoyer</b>\n"
        "⚠️ Le message sera immédiatement envoyé à l'utilisateur.",
        reply_markup=profile_search_return_finl(user_id),
    )


# Réception du message à envoyer à l'utilisateur
@router.message(F.text, StateFilter("here_profile_message"))
async def functions_profile_user_message_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    user_id = (await state.get_data())['here_profile']
    await state.clear()

    get_message = "<b>💌 Message de l'administrateur:</b>\n" + f"<code>{clear_html(message.text)}</code>"
    get_user = Userx.get(user_id=user_id)

    try:
        await bot.send_message(user_id, get_message)
    except:
        await message.answer(
            f"👤 Utilisateur: <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>\n"
            f"❌ Impossible d'envoyer le message. L'utilisateur a peut-être bloqué le bot."
        )
    else:
        await message.answer(
            f"👤 Utilisateur: <a href='tg://user?id={get_user.user_id}'>{get_user.user_name}</a>\n"
            f"💌 Message envoyé : {get_message}"
        )

    await open_profile_admin(bot, message.from_user.id, get_user)
