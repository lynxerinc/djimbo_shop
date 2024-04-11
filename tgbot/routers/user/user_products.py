# - *- coding: utf- 8 - *-
import asyncio

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from tgbot.database.db_position import Positionx
from tgbot.database.db_purchases import Purchasesx
from tgbot.database.db_users import Userx
from tgbot.keyboards.inline_user import products_confirm_finl, products_return_finl
from tgbot.keyboards.inline_user_page import *
from tgbot.keyboards.reply_main import menu_frep
from tgbot.utils.const_functions import split_messages, get_unix, ded, del_message, convert_date, gen_id
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import get_positions_items
from tgbot.utils.text_functions import position_open_user

router = Router(name=__name__)


# Pages de choix de catégorie pour l'achat de produits
@router.callback_query(F.data.startswith("buy_category_swipe:"))
async def user_buy_category_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>🎁 Choisissez le produit que vous souhaitez :</b>",
        reply_markup=prod_item_category_swipe_fp(remover),
    )


# Ouverture de catégorie avec choix de position pour l'achat de produit
@router.callback_query(F.data.startswith("buy_category_open:"))
async def user_buy_category_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_category = Categoryx.get(category_id=category_id)
    get_positions = get_positions_items(category_id)

    if len(get_positions) >= 1:
        await del_message(call.message)

        await call.message.answer(
            f"<b>🎁 Catégorie actuelle : <code>{get_category.category_name}</code></b>",
            reply_markup=prod_item_position_swipe_fp(remover, category_id),
        )
    else:
        if remover == 0:
            await call.message.edit_text("<b>🎁 Désolé, il n'y a pas de produits disponibles en ce moment.</b>")
            await call.answer("❗ Les positions ont été modifiées ou supprimées")
        else:
            await call.answer(
                f"❕ Il n'y a pas de produits dans la catégorie {get_category.category_name}",
                True,
                cache_time=5,
            )


# Pages de choix de position pour l'achat de produit
@router.callback_query(F.data.startswith("buy_position_swipe:"))
async def user_buy_position_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_category = Categoryx.get(category_id=category_id)

    await del_message(call.message)
    await call.message.answer(
        f"<b>🎁 Catégorie actuelle : <code>{get_category.category_name}</code></b>",
        reply_markup=prod_item_position_swipe_fp(remover, category_id),
    )


# Ouverture de position pour l'achat
@router.callback_query(F.data.startswith("buy_position_open:"))
async def user_buy_position_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await state.clear()

    await del_message(call.message)
    await position_open_user(bot, call.from_user.id, position_id, remover)


#################################### ACHAT ###################################
# Choix du nombre de produits à acheter
@router.callback_query(F.data.startswith("buy_item_open:"))
async def user_buy_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_position = Positionx.get(position_id=position_id)
    get_items = Itemx.gets(position_id=position_id)
    get_user = Userx.get(user_id=call.from_user.id)

    # Vérification si le solde de l'utilisateur est suffisant
    if int(get_user.user_balance) < int(get_position.position_price):
        return await call.answer("❗ Vous n'avez pas assez de fonds. Veuillez recharger votre solde", True)

    if len(get_items) < 1:
        return await call.answer("❗ Il n'y a pas de produits disponibles", True)

    # Nombre maximum de produits pouvant être achetés, ajusté selon le solde de l'utilisateur
    if get_position.position_price != 0:
        get_count = round(int(get_user.user_balance / get_position.position_price), 2)

        if get_count > len(get_items):
            get_items = len(get_items)
        else:
            get_items = get_count
    else:
        get_items = len(get_items)

    # Si un seul produit est disponible, passer la saisie du nombre de produits à acheter
    if get_items == 1:
        await state.clear()

        await del_message(call.message)

        await call.message.answer(
            ded(f"""
                <b>🎁 Voulez-vous vraiment acheter le(s) produit(s) ?</b>
                ➖➖➖➖➖➖➖➖➖➖
                ▪️ Produit : <code>{get_position.position_name}</code>
                ▪️ Quantité : <code>1pc</code>
                ▪️ Somme à payer : <code>{get_position.position_price}€</code>
            """),
            reply_markup=products_confirm_finl(position_id, get_position.category_id, 1),
        )
    else:
        await state.update_data(here_buy_position_id=position_id)
        await state.set_state("here_item_count")

        await del_message(call.message)

        await call.message.answer(
            ded(f"""
                <b>🎁 Entrez le nombre de produits à acheter</b>
                ❕ De <code>1</code> à <code>{get_items}</code>
                ➖➖➖➖➖➖➖➖➖➖
                ▪️ Produit : <code>{get_position.position_name}</code> - <code>{get_position.position_price}€</code>
                ▪️ Votre solde : <code>{get_user.user_balance}€</code>
            """),
            reply_markup=products_return_finl(position_id, get_position.category_id),
        )


# Acceptation du nombre de produits à acheter
@router.message(F.text, StateFilter("here_item_count"))
async def user_buy_count(message: Message, bot: Bot, state: FSM, arSession: ARS):
    position_id = (await state.get_data())['here_buy_position_id']

    get_position = Positionx.get(position_id=position_id)
    get_user = Userx.get(user_id=message.from_user.id)
    get_items = Itemx.gets(position_id=position_id)

    # Nombre maximum de produits pouvant être achetés, ajusté selon le solde de l'utilisateur
    if get_position.position_price != 0:
        get_count = int(get_user.user_balance / get_position.position_price)

        if get_count > len(get_items):
            get_count = len(get_items)
    else:
        get_count = len(get_items)

    send_message = ded(f"""
        🎁 Entrez le nombre de produits à acheter
        ❕ De <code>1</code> à <code>{get_count}</code>
        ➖➖➖➖➖➖➖➖➖➖
        ▪️ Produit : <code>{get_position.position_name}</code> - <code>{get_position.position_price}€</code>
        ▪️ Votre solde : <code>{get_user.user_balance}€</code>
    """)

    # Si un nombre n'a pas été entré
    if not message.text.isdigit():
        return await message.answer(
            f"<b>❌ Les données ont été entrées incorrectement.</b>\n" + send_message,
            reply_markup=products_return_finl(position_id, get_position.category_id),
        )

    get_count = int(message.text)
    amount_pay = round(get_position.position_price * get_count, 2)

    # Si il n'y a pas de produits disponibles
    if len(get_items) < 1:
        await state.clear()
        return await message.answer("<b>🎁 Le produit que vous vouliez acheter est épuisé</b>")

    # Si le nombre de produits est inférieur à 1 ou supérieur à la disponibilité
    if get_count < 1 or get_count > len(get_items):
        return await message.answer(
            f"<b>❌ Quantité de produits incorrecte.</b>\n" + send_message,
            reply_markup=products_return_finl(position_id, get_position.category_id),
        )

    # Si le solde de l'utilisateur est inférieur au prix total de l'achat
    if int(get_user.user_balance) < amount_pay:
        return await message.answer(
            f"<b>❌ Fonds insuffisants sur votre compte.</b>\n" + send_message,
            reply_markup=products_return_finl(position_id, get_position.category_id),
        )

    await state.clear()

    await message.answer(
        ded(f"""
            <b>🎁 Voulez-vous vraiment acheter le(s) produit(s) ?</b>
            ➖➖➖➖➖➖➖➖➖➖
            ▪️ Produit : <code>{get_position.position_name}</code>
            ▪️ Quantité : <code>{get_count}pcs</code>
            ▪️ Somme totale : <code>{amount_pay}€</code>
        """),
        reply_markup=products_confirm_finl(position_id, get_position.category_id, get_count),
    )


# Confirmation de l'achat du produit
@router.callback_query(F.data.startswith("buy_item_confirm:"))
async def user_buy_confirm(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = int(call.data.split(":")[1])
    purchase_count = int(call.data.split(":")[2])

    get_items = Itemx.gets(position_id=position_id)

    # Vérification de la disponibilité du nombre requis de produits
    if purchase_count > len(get_items):
        return await call.message.edit_text(
            "<b>🎁 Le produit que vous souhaitiez acheter est épuisé ou a été modifié.</b>",
        )

    await call.message.edit_text("<b>🔄 Attendez, les produits sont en préparation</b>")

    get_position = Positionx.get(position_id=position_id)
    get_category = Categoryx.get(category_id=get_position.category_id)
    get_user = Userx.get(user_id=call.from_user.id)

    purchase_price = round(get_position.position_price * purchase_count, 2)

    # Vérification du solde de l'utilisateur et du montant total de l'achat
    if get_user.user_balance < purchase_price:
        return await call.message.answer("<b>❗ Vous n'avez pas assez de fonds sur votre compte</b>")

    save_items, save_len = Itemx.buy(get_items, purchase_count)
    save_count = len(save_items)

    # Si le stock s'avère inférieur au nombre demandé
    if purchase_count != save_count:
        purchase_price = round(get_position.position_price * save_count, 2)
        purchase_count = save_count

    Userx.update(
        get_user.user_id,
        user_balance=round(get_user.user_balance - purchase_price, 2),
    )

    purchase_receipt = gen_id()
    purchase_unix = get_unix()
    purchase_data = "\n".join(save_items)

    Purchasesx.add(
        get_user.user_id,
        get_user.user_balance,
        round(get_user.user_balance - purchase_price, 2),
        purchase_receipt,
        purchase_data,
        purchase_count,
        purchase_price,
        get_position.position_price,
        get_position.position_id,
        get_position.position_name,
        get_category.category_id,
        get_category.category_name,
    )

    await del_message(call.message)

    for item in split_messages(save_items, save_len):
        await call.message.answer("\n\n".join(item), parse_mode="None")
        await asyncio.sleep(0.3)

    await call.message.answer(
        ded(f"""
            <b>✅ Vous avez réussi à acheter le(s) produit(s)</b>
            ➖➖➖➖➖➖➖➖➖➖
            ▪️ Reçu : <code>#{purchase_receipt}</code>
            ▪️ Produit : <code>{get_position.position_name} | {purchase_count}pcs | {purchase_price}€</code>
            ▪️ Date d'achat : <code>{convert_date(purchase_unix)}</code>
        """),
        reply_markup=menu_frep(call.from_user.id),
    )
