# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from tgbot.database.db_category import Categoryx
from tgbot.database.db_item import Itemx
from tgbot.database.db_position import Positionx
from tgbot.database.db_users import Userx
from tgbot.keyboards.inline_admin import close_finl
from tgbot.keyboards.inline_admin_page import (category_edit_swipe_fp, position_add_swipe_fp,
                                               position_edit_category_swipe_fp, position_edit_swipe_fp,
                                               item_add_position_swipe_fp, item_add_category_swipe_fp,
                                               item_delete_swipe_fp)
from tgbot.keyboards.inline_admin_prod import (category_edit_delete_finl, position_edit_clear_finl,
                                               position_edit_delete_finl, position_edit_cancel_finl,
                                               category_edit_cancel_finl, products_removes_finl,
                                               products_removes_categories_finl, products_removes_positions_finl,
                                               products_removes_items_finl, item_add_finish_finl)
from tgbot.utils.const_functions import clear_list, is_number, to_number, del_message, ded, get_unix, clear_html
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import upload_text, upload_photo
from tgbot.utils.text_functions import category_open_admin, position_open_admin, item_open_admin

router = Router(name=__name__)


# Création d'une nouvelle catégorie
@router.message(F.text == "🗃 Créer une catégorie ➕")
async def prod_category_add(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await state.set_state("here_category_name")
    await message.answer("<b>🗃 Entrez le nom pour la catégorie</b>")


# Sélection d'une catégorie pour édition
@router.message(F.text == "🗃 Modifier une catégorie 🖍")
async def prod_category_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>🗃 Sélectionnez une catégorie à modifier 🖍</b>",
            reply_markup=category_edit_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Il n'y a pas de catégories à modifier</b>")


# Création d'une nouvelle position
@router.message(F.text == "📁 Créer une position ➕")
async def prod_position_add(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>📁 Sélectionnez une catégorie pour la position ➕</b>",
            reply_markup=position_add_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Il n'y a pas de catégories pour créer une position</b>")


# Sélection d'une position pour édition
@router.message(F.text == "📁 Modifier une position 🖍")
async def prod_position_edit(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>📁 Sélectionnez une position à modifier 🖍</b>",
            reply_markup=position_edit_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Il n'y a pas de catégories pour modifier les positions</b>")


# Pages de produits à ajouter
@router.message(F.text == "🎁 Ajouter des produits ➕")
async def prod_item_add(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await message.answer(
            "<b>🎁 Sélectionnez une position pour les produits ➕</b>",
            reply_markup=item_add_category_swipe_fp(0),
        )
    else:
        await message.answer("<b>❌ Il n'y a pas de positions pour ajouter des produits</b>")


# Suppression de catégories, positions ou produits
@router.message(F.text == "❌ Suppression")
async def prod_removes(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🎁 Sélectionnez la section que vous souhaitez supprimer ❌</b>\n",
        reply_markup=products_removes_finl(),
    )


################################################################################
############################### CRÉATION DE CATÉGORIES #########################
# Acceptation du nom de la catégorie pour sa création
@router.message(F.text, StateFilter('here_category_name'))
async def prod_category_add_name_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    if len(message.text) > 50:
        return await message.answer(
            "<b>❌ Le nom ne peut dépasser 50 caractères.</b>\n"
            "🗃 Entrez le nom pour la catégorie",
        )

    await state.clear()

    category_id = get_unix()
    Categoryx.add(category_id, clear_html(message.text))

    await category_open_admin(bot, message.from_user.id, category_id, 0)
    

################################################################################
############################### MODIFICATION DE CATÉGORIE ######################
# Page de sélection des catégories à modifier
@router.callback_query(F.data.startswith("catategory_edit_swipe:"))
async def prod_category_edit_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>🗃 Choisissez une catégorie à modifier 🖍</b>",
        reply_markup=category_edit_swipe_fp(remover),
    )


# Choix de la catégorie actuelle pour modification
@router.callback_query(F.data.startswith("category_edit_open:"))
async def prod_category_edit_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await state.clear()

    await del_message(call.message)
    await category_open_admin(bot, call.from_user.id, category_id, remover)


############################ MODIFICATION DE LA CATÉGORIE PROPREMENT DITE #######
# Modification du nom de la catégorie
@router.callback_query(F.data.startswith("category_edit_name:"))
async def prod_category_edit_name(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_category_edit_name")

    await del_message(call.message)

    await call.message.answer(
        "<b>🗃 Entrez le nouveau nom pour la catégorie</b>",
        reply_markup=category_edit_cancel_finl(category_id, remover),
    )


# Acceptation du nouveau nom pour la catégorie
@router.message(F.text, StateFilter('here_category_edit_name'))
async def prod_category_edit_name_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    category_id = (await state.get_data())['here_category_id']
    remover = (await state.get_data())['here_remover']

    if len(message.text) > 50:
        return await message.answer(
            "<b>❌ Le nom ne peut dépasser 50 caractères.</b>\n"
            "🗃 Entrez le nouveau nom pour la catégorie",
            reply_markup=category_edit_cancel_finl(category_id, remover),
        )

    await state.clear()

    Categoryx.update(category_id, category_name=clear_html(message.text))
    await category_open_admin(bot, message.from_user.id, category_id, remover)


# Fenêtre de confirmation pour supprimer la catégorie
@router.callback_query(F.data.startswith("category_edit_delete:"))
async def prod_category_edit_delete(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await call.message.edit_text(
        "<b>❗ Voulez-vous vraiment supprimer cette catégorie et toutes ses données ?</b>",
        reply_markup=category_edit_delete_finl(category_id, remover),
    )


# Confirmation de la suppression de la catégorie
@router.callback_query(F.data.startswith("category_edit_delete_confirm:"))
async def prod_category_edit_delete_confirm(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    Categoryx.delete(category_id=category_id)
    Positionx.delete(category_id=category_id)
    Itemx.delete(category_id=category_id)

    await call.answer("🗃 La catégorie et toutes ses données ont été supprimées avec succès ✅")

    get_categories = Categoryx.get_all()

    if len(get_categories) >= 1:
        await call.message.edit_text(
            "<b>🗃 Choisissez une catégorie à modifier 🖍</b>",
            reply_markup=category_edit_swipe_fp(remover),
        )
    else:
        await del_message(call.message)


################################################################################
############################### AJOUT DE POSITION ##############################
# Page suivante pour choisir la catégorie où placer la position
@router.callback_query(F.data.startswith("position_add_swipe:"))
async def prod_position_add_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>📁 Choisissez une catégorie pour la position ➕</b>",
        reply_markup=position_add_swipe_fp(remover),
    )


# Sélection d'une catégorie pour créer une position
@router.callback_query(F.data.startswith("position_add_open:"))
async def prod_position_add_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]

    await state.update_data(here_category_id=category_id)
    await state.set_state("here_position_name")

    await call.message.edit_text("<b>📁 Entrez le nom pour la position</b>")


# Acceptation du nom pour la création de la position
@router.message(F.text, StateFilter('here_position_name'))
async def prod_position_add_name_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    if len(message.text) > 50:
        return await message.answer(
            "<b>❌ Le nom ne peut dépasser 50 caractères.</b>\n"
            "📁 Entrez le nom pour la position",
        )

    await state.update_data(here_position_name=clear_html(message.text))
    await state.set_state("here_position_price")

    await message.answer("<b>📁 Entrez le prix pour la position</b>")


# Acceptation du prix pour la création de la position
@router.message(F.text, StateFilter('here_position_price'))
async def prod_position_add_price_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    if not is_number(message.text):
        return await message.answer(
            "<b>❌ Les données ont été saisies incorrectement.</b>\n"
            "📁 Entrez le prix pour la position",
        )

    if to_number(message.text) > 10_000_000 or to_number(message.text) < 0:
        return await message.answer(
            "<b>❌ Le prix ne peut être inférieur à 0 ou supérieur à 10 000 000₽.</b>\n"
            "📁 Entrez le prix pour la position",
        )

    await state.update_data(here_position_price=to_number(message.text))
    await state.set_state("here_position_desc")

    await message.answer(
        "<b>📁 Entrez la description pour la position</b>\n"
        "❕ Vous pouvez utiliser le balisage HTML\n"
        "❕ Envoyez <code>0</code> pour passer.",
    )


# Acceptation de la description pour la création de la position
@router.message(F.text, StateFilter('here_position_desc'))
async def prod_position_add_desc_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    if len(message.text) > 400:
        await message.answer(
            "<b>❌ La description ne peut dépasser 400 caractères.</b>\n"
            "📁 Entrez une nouvelle description pour la position\n"
            "❕ Vous pouvez utiliser le balisage HTML\n"
            "❕ Envoyez <code>0</code> pour passer.",
        )

    try:
        if message.text != "0":
            await (await message.answer(message.text)).delete()

            position_desc = message.text
        else:
            position_desc = "None"
    except:
        return await message.answer(
            "<b>❌ Erreur de syntaxe HTML.</b>\n"
            "📁 Entrez la description pour la position\n"
            "❕ Vous pouvez utiliser le balisage HTML\n"
            "❕ Envoyez <code>0</code> pour passer.",
        )

    await state.update_data(here_position_desc=position_desc)
    await state.set_state("here_position_photo")

    await message.answer(
        "<b>📁 Envoyez une image pour la position</b>\n"
        "❕ Envoyez <code>0</code> pour passer.",
    )


# Acceptation de l'image pour la création de la position
@router.message((F.text == "0") | F.photo, StateFilter('here_position_photo'))
async def prod_position_add_photo_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    state_data = await state.get_data()

    category_id = state_data['here_category_id']
    position_name = clear_html(state_data['here_position_name'])
    position_price = to_number(state_data['here_position_price'])
    position_desc = state_data['here_position_desc']
    position_id = get_unix()
    await state.clear()

    if message.photo is not None:
        file_path = (await bot.get_file(message.photo[-1].file_id)).file_path
        photo_path = await bot.download_file(file_path)

        position_photo = await upload_photo(arSession, photo_path)
    else:
        position_photo = "None"

    Positionx.add(
        category_id,
        position_id,
        position_name,
        position_price,
        position_desc,
        position_photo,
    )

    await position_open_admin(bot, message.from_user.id, position_id)


################################################################################
############################### MODIFICATION DE POSITION ########################
# Défilement des pages de catégories pour la modification d'une position
@router.callback_query(F.data.startswith("position_edit_category_swipe:"))
async def prod_position_edit_category_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>📁 Choisissez la position à modifier 🖍</b>",
        reply_markup=position_edit_category_swipe_fp(remover),
    )


# Sélection d'une catégorie contenant la position à modifier
@router.callback_query(F.data.startswith("position_edit_category_open:"))
async def prod_position_edit_category_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]

    get_category = Categoryx.get(category_id=category_id)
    get_positions = Positionx.gets(category_id=category_id)

    if len(get_positions) >= 1:
        await call.message.edit_text(
            "<b>📁 Choisissez la position à modifier 🖍</b>",
            reply_markup=position_edit_swipe_fp(0, category_id),
        )
    else:
        await call.answer(f"📁 Aucune position dans la catégorie {get_category.category_name}")


# Défilement des pages de positions pour la modification
@router.callback_query(F.data.startswith("position_edit_swipe:"))
async def prod_position_edit_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Choisissez la position à modifier 🖍</b>",
        reply_markup=position_edit_swipe_fp(remover, category_id),
    )


# Sélection de la position pour la modifier
@router.callback_query(F.data.startswith("position_edit_open:"))
async def prod_position_edit_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.clear()

    await del_message(call.message)
    await position_open_admin(bot, call.from_user.id, position_id)


############################ MODIFICATION PROPRE DE LA POSITION ################
# Modification du nom de la position
@router.callback_query(F.data.startswith("position_edit_name:"))
async def prod_position_edit_name(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_position_id=position_id)
    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_position_edit_name")

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Entrez le nouveau nom pour la position</b>",
        reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
    )


# Acceptation du nouveau nom pour la position
@router.message(F.text, StateFilter('here_position_edit_name'))
async def prod_position_edit_name_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    state_data = await state.get_data()

    position_id = state_data['here_position_id']
    category_id = state_data['here_category_id']
    remover = state_data['here_remover']

    if len(message.text) > 50:
        return await message.answer(
            "<b>❌ Le nom ne peut dépasser 50 caractères.</b>\n"
            "📁 Entrez le nouveau nom pour la position",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    await state.clear()

    Positionx.update(position_id, position_name=clear_html(message.text))
    await position_open_admin(bot, message.from_user.id, position_id)


# Modification du prix de la position
@router.callback_query(F.data.startswith("position_edit_price:"))
async def prod_position_edit_price(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_position_id=position_id)
    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_position_edit_price")

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Entrez le nouveau prix pour la position</b>",
        reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
    )


# Acceptation du nouveau prix pour la position
@router.message(F.text, StateFilter('here_position_edit_price'))
async def prod_position_edit_price_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    state_data = await state.get_data()

    position_id = state_data['here_position_id']
    category_id = state_data['here_category_id']
    remover = state_data['here_remover']

    if not is_number(message.text):
        await message.answer(
            "<b>❌ Les données ont été saisies incorrectement.</b>\n"
            "📁 Entrez le prix pour la position",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    if to_number(message.text) > 10_000_000 or to_number(message.text) < 0:
        await message.answer(
            "<b>❌ Le prix ne peut être inférieur à 0 ou supérieur à 10 000 000₽.</b>\n"
            "📁 Entrez le prix pour la position",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    await state.clear()

    Positionx.update(position_id, position_price=to_number(message.text))
    await position_open_admin(bot, message.from_user.id, position_id)


# Modification de la description de la position
@router.callback_query(F.data.startswith("position_edit_desc:"))
async def prod_position_edit_desc(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_position_id=position_id)
    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_position_edit_desc")

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Entrez la nouvelle description pour la position</b>\n"
        "❕ Vous pouvez utiliser la syntaxe HTML\n"
        "❕ Envoyez <code>0</code> pour passer.",
        reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
    )


# Acceptation de la nouvelle description pour la position
@router.message(F.text, StateFilter('here_position_edit_desc'))
async def prod_position_edit_desc_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    state_data = await state.get_data()

    position_id = state_data['here_position_id']
    category_id = state_data['here_category_id']
    remover = state_data['here_remover']

    if len(message.text) > 400:
        return await message.answer(
            "<b>❌ La description ne peut dépasser 400 caractères.</b>\n"
            "📁 Entrez la nouvelle description pour la position\n"
            "❕ Vous pouvez utiliser la syntaxe HTML\n"
            "❕ Envoyez <code>0</code> pour passer.",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    try:
        if message.text != "0":
            await (await message.answer(message.text)).delete()

            position_desc = message.text
        else:
            position_desc = "None"
    except:
        return await message.answer(
            "<b>❌ Erreur de syntaxe HTML.</b>\n"
            "📁 Entrez la nouvelle description pour la position\n"
            "❕ Vous pouvez utiliser la syntaxe HTML\n"
            "❕ Envoyez <code>0</code> pour passer.",
            reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
        )

    await state.clear()

    Positionx.update(position_id, position_desc=position_desc)
    await position_open_admin(bot, message.from_user.id, position_id)


# Modification de l'image de la position
@router.callback_query(F.data.startswith("position_edit_photo:"))
async def prod_position_edit_photo(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await state.update_data(here_position_id=position_id)
    await state.update_data(here_category_id=category_id)
    await state.update_data(here_remover=remover)
    await state.set_state("here_position_edit_photo")

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Envoyez la nouvelle image pour la position</b>\n"
        "❕ Envoyez <code>0</code> pour ignorer.",
        reply_markup=position_edit_cancel_finl(position_id, category_id, remover),
    )


# Acceptation de la nouvelle image pour la position
@router.message((F.text == "0") | F.photo, StateFilter('here_position_edit_photo'))
async def prod_position_edit_photo_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    state_data = await state.get_data()
    await state.clear()

    position_id = state_data['here_position_id']
    category_id = state_data['here_category_id']
    remover = state_data['here_remover']

    if message.photo is not None:
        file_path = (await bot.get_file(message.photo[-1].file_id)).file_path
        photo_path = await bot.download_file(file_path)

        position_photo = await upload_photo(arSession, photo_path)
    else:
        position_photo = "None"

    Positionx.update(position_id, position_photo=position_photo)
    await position_open_admin(bot, message.from_user.id, position_id)


# Exportation des produits
@router.callback_query(F.data.startswith("position_edit_items:"))
async def prod_position_edit_items(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    get_position = Positionx.get(position_id=position_id)
    get_items = Itemx.gets(position_id=position_id)

    if len(get_items) >= 1:
        save_items = "\n\n".join([item.item_data for item in get_items])
        save_items = await upload_text(arSession, save_items)

        await call.message.answer(
            f"<b>📥 Tous les produits de la position: <code>{get_position.position_name}</code>\n"
            f"🔗 Lien: <a href='{save_items}'>cliquable</a></b>",
            reply_markup=close_finl(),
        )
        await call.answer(cache_time=5)
    else:
        await call.answer("❕ Aucun produit dans cette position", True)


# Suppression de la position
@router.callback_query(F.data.startswith("position_edit_delete:"))
async def prod_position_edit_delete(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Voulez-vous vraiment supprimer cette position ? ❌</b>",
        reply_markup=position_edit_delete_finl(position_id, category_id, remover),
    )


# Confirmation de la suppression de la position
@router.callback_query(F.data.startswith("position_edit_delete_confirm:"))
async def prod_position_edit_delete_confirm(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    Itemx.delete(position_id=position_id)
    Positionx.delete(position_id=position_id)

    await call.answer("📁 La position et ses produits ont été supprimés avec succès ✅")

    if len(Positionx.gets(category_id=category_id)) >= 1:
        await call.message.edit_text(
            "<b>📁 Choisissez une position à modifier 🖍</b>",
            reply_markup=position_edit_swipe_fp(remover, category_id),
        )
    else:
        await del_message(call.message)


# Nettoyage de la position
@router.callback_query(F.data.startswith("position_edit_clear:"))
async def prod_position_edit_clear(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    await del_message(call.message)

    await call.message.answer(
        "<b>📁 Souhaitez-vous supprimer tous les produits de cette position ?</b>",
        reply_markup=position_edit_clear_finl(position_id, category_id, remover),
    )


# Accord pour le nettoyage de la position
@router.callback_query(F.data.startswith("position_edit_clear_confirm:"))
async def prod_position_edit_clear_confirm(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    Itemx.delete(position_id=position_id)
    await call.answer("📁 Tous les produits de la position ont été supprimés avec succès ✅")

    await del_message(call.message)
    await position_open_admin(bot, call.from_user.id, position_id)


################################################################################
############################### AJOUT DE PRODUITS ##############################
# Navigation entre les pages de catégories pour l'ajout de produits
@router.callback_query(F.data.startswith("item_add_category_swipe:"))
async def prod_item_add_category_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>🎁 Choisissez une position pour les produits ➕</b>",
        reply_markup=item_add_category_swipe_fp(remover),
    )


# Sélection d'une catégorie contenant la position souhaitée
@router.callback_query(F.data.startswith("item_add_category_open:"))
async def prod_item_add_category_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    get_category = Categoryx.get(category_id=category_id)
    get_positions = Positionx.gets(category_id=category_id)

    await del_message(call.message)

    if len(get_positions) >= 1:
        await call.message.answer(
            "<b>🎁 Choisissez une position pour les produits ➕</b>",
            reply_markup=item_add_position_swipe_fp(0, category_id),
        )
    else:
        await call.answer(f"🎁 Aucune position dans la catégorie {get_category.category_name}")


# Navigation entre les pages de positions pour l'ajout de produits
@router.callback_query(F.data.startswith("item_add_position_swipe:"))
async def prod_item_add_position_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    category_id = call.data.split(":")[1]
    remover = int(call.data.split(":")[2])

    await call.message.edit_text(
        "<b>🎁 Choisissez une position pour les produits ➕</b>",
        reply_markup=item_add_position_swipe_fp(remover, category_id),
    )


# Sélection d'une position pour l'ajout de produits
@router.callback_query(F.data.startswith("item_add_position_open:"), flags={'rate': 0})
async def prod_item_add_position_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]

    await state.update_data(here_add_item_category_id=category_id)
    await state.update_data(here_add_item_position_id=position_id)
    await state.update_data(here_add_item_count=0)
    await state.set_state("here_add_items")

    await del_message(call.message)

    await call.message.answer(
        ded(f"""
            <b>📤 Envoyez les données des produits.</b>
            ❗ Les produits doivent être séparés par une ligne vide. Exemple:
            <code>Données du produit...

            Données du produit...

            Données du produit...</code>
        """),
        reply_markup=item_add_finish_finl(position_id),
    )


# Fin de l'ajout des produits
@router.callback_query(F.data.startswith('item_add_position_finish:'), flags={'rate': 0})
async def prod_item_add_finish(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]

    try:
        count_items = (await state.get_data())['here_add_item_count']
    except:
        count_items = 0

    await state.clear()

    await call.message.edit_reply_markup()
    await call.message.answer(
        "<b>📥 L'ajout des produits a été complété avec succès ✅\n"
        f"🎁 Nombre de produits ajoutés: <code>{count_items}</code></b>",
    )

    await position_open_admin(bot, call.from_user.id, position_id)


# Réception des données des produits
@router.message(F.text, StateFilter('here_add_items'), flags={'rate': 0})
async def prod_item_add_get(message: Message, bot: Bot, state: FSM, arSession: ARS):
    cache_message = await message.answer("<b>⌛ Veuillez patienter, ajout des produits en cours...</b>")

    count_add = 0
    get_items = clear_list(message.text.split("\n\n"))

    for check_item in get_items:
        if not check_item.isspace() and check_item != "":
            count_add += 1

    count_item = (await state.get_data())['here_add_item_count']
    category_id = (await state.get_data())['here_add_item_category_id']
    position_id = (await state.get_data())['here_add_item_position_id']

    await state.update_data(here_add_item_count=count_item + count_add)

    get_user = Userx.get(user_id=message.from_user.id)
    Itemx.add(
        get_user.user_id,
        category_id,
        position_id,
        get_items,
    )

    await cache_message.edit_text(
        f"<b>📥 <u>{count_add} produits</u> ont été ajoutés avec succès ✅</b>",
        reply_markup=item_add_finish_finl(position_id),
    )



################################################################################
############################### SUPPRESSION DES PRODUITS #######################
# Pages pour la suppression des produits
@router.callback_query(F.data.startswith("item_delete_swipe:"))
async def prod_item_delete_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    position_id = call.data.split(":")[1]
    category_id = call.data.split(":")[2]
    remover = int(call.data.split(":")[3])

    get_items = Itemx.gets(position_id=position_id)
    get_position = Positionx.get(position_id=position_id)

    await del_message(call.message)

    if len(get_items) >= 1:
        await call.message.answer(
            "<b>🎁 Choisissez un produit à supprimer</b>",
            reply_markup=item_delete_swipe_fp(remover, position_id, category_id),
        )
    else:
        await call.answer(f"🎁 Aucun produit dans la position {get_position.position_name}")


# Suppression d'un produit
@router.callback_query(F.data.startswith("item_delete_open:"))
async def prod_item_delete_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    item_id = call.data.split(":")[1]

    await del_message(call.message)
    await item_open_admin(bot, call.from_user.id, item_id, 0)


# Confirmation de la suppression d'un produit
@router.callback_query(F.data.startswith("item_delete_confirm:"))
async def prod_item_delete_confirm_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    item_id = call.data.split(":")[1]

    get_item = Itemx.get(item_id=item_id)
    get_items = Itemx.gets(position_id=get_item.position_id)

    Itemx.delete(item_id=item_id)

    await call.message.edit_text(
        f"<b>✅ Le produit a été supprimé avec succès</b>\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"🎁 Produit: <code>{get_item.item_data}</code>"
    )

    if len(get_items) >= 1:
        await call.message.answer(
            "<b>🎁 Choisissez un produit à supprimer</b>",
            reply_markup=item_delete_swipe_fp(0, get_item.position_id, get_item.category_id),
        )


################################################################################
############################### SUPPRESSION DES SECTIONS #######################
# Retour au menu de suppression des sections
@router.callback_query(F.data == "prod_removes_return")
async def prod_removes_return(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await call.message.edit_text(
        "<b>🎁 Choisissez la section que vous souhaitez supprimer ❌</b>\n",
        reply_markup=products_removes_finl(),
    )


# Suppression de toutes les catégories
@router.callback_query(F.data == "prod_removes_categories")
async def prod_removes_categories(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_categories = len(Categoryx.get_all())
    get_positions = len(Positionx.get_all())
    get_items = len(Itemx.get_all())

    await call.message.edit_text(
        f"<b>❌ Voulez-vous vraiment supprimer toutes les catégories, positions et produits ?</b>\n"
        f"🗃 Catégories: <code>{get_categories}</code>\n"
        f"📁 Positions: <code>{get_positions}</code>\n"
        f"🎁 Produits: <code>{get_items}</code>",
        reply_markup=products_removes_categories_finl(),
    )


# Confirmation de la suppression de toutes les catégories (incluant positions et produits)
@router.callback_query(F.data == "prod_removes_categories_confirm")
async def prod_removes_categories_confirm(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_categories = len(Categoryx.get_all())
    get_positions = len(Positionx.get_all())
    get_items = len(Itemx.get_all())

    Categoryx.clear()
    Positionx.clear()
    Itemx.clear()

    await call.message.edit_text(
        f"<b>✅ Vous avez réussi à supprimer toutes les catégories</b>\n"
        f"🗃 Catégories: <code>{get_categories}</code>\n"
        f"📁 Positions: <code>{get_positions}</code>\n"
        f"🎁 Produits: <code>{get_items}</code>"
    )


# Suppression de toutes les positions
@router.callback_query(F.data == "prod_removes_positions")
async def prod_removes_positions(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_positions = len(Positionx.get_all())
    get_items = len(Itemx.get_all())

    await call.message.edit_text(
        f"<b>❌ Voulez-vous vraiment supprimer toutes les positions et les produits associés ?</b>\n"
        f"📁 Positions: <code>{get_positions}</code>\n"
        f"🎁 Produits: <code>{get_items}</code>",
        reply_markup=products_removes_positions_finl(),
    )


# Confirmation de la suppression de toutes les positions (et produits associés)
@router.callback_query(F.data == "prod_removes_positions_confirm")
async def prod_position_remove(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_positions = len(Positionx.get_all())
    get_items = len(Itemx.get_all())

    Positionx.clear()
    Itemx.clear()

    await call.message.edit_text(
        f"<b>✅ Vous avez réussi à supprimer toutes les positions</b>\n"
        f"📁 Positions: <code>{get_positions}</code>\n"
        f"🎁 Produits: <code>{get_items}</code>"
    )


# Suppression de tous les produits
@router.callback_query(F.data == "prod_removes_items")
async def prod_removes_items(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_items = len(Itemx.get_all())

    await call.message.edit_text(
        f"<b>❌ Voulez-vous vraiment supprimer tous les produits ?</b>\n"
        f"🎁 Produits: <code>{get_items}</code>",
        reply_markup=products_removes_items_finl(),
    )


# Accord pour la suppression de tous les produits
@router.callback_query(F.data == "prod_removes_items_confirm")
async def prod_item_remove(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    get_items = len(Itemx.get_all())

    Itemx.clear()

    await call.message.edit_text(
        f"<b>✅ Vous avez réussi à supprimer tous les produits</b>\n"
        f"🎁 Produits: <code>{get_items}</code>"
    )
