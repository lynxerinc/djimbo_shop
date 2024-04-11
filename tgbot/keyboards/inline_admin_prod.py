# - *- coding: utf- 8 - *-
from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils.const_functions import ikb


################################### CATÉGORIES ##################################
# Modification de catégorie
def category_edit_open_finl(category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("▪️ Modifier le nom", data=f"category_edit_name:{category_id}:{remover}"),
        ikb("▪️ Ajouter une position", data=f"position_add_open:{category_id}"),
    ).row(
        ikb("🔙 Retour", data=f"catategory_edit_swipe:{remover}"),
        ikb("▪️ Supprimer", data=f"category_edit_delete:{category_id}:{remover}")
    )

    return keyboard.as_markup()


# Confirmation de la suppression de la catégorie
def category_edit_delete_finl(category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Oui, supprimer", data=f"category_edit_delete_confirm:{category_id}:{remover}"),
        ikb("❌ Non, annuler", data=f"category_edit_open:{category_id}:{remover}")
    )

    return keyboard.as_markup()


# Annulation de la modification de la catégorie et retour
def category_edit_cancel_finl(category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("❌ Annuler", data=f"category_edit_open:{category_id}:{remover}"),
    )

    return keyboard.as_markup()


#################################### POSITIONS ###################################
# Boutons lors de l'ouverture d'une position pour modification
def position_edit_open_finl(position_id, category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("▪️ Modifier le nom", data=f"position_edit_name:{position_id}:{category_id}:{remover}"),
        ikb("▪️ Modifier le prix", data=f"position_edit_price:{position_id}:{category_id}:{remover}"),
    ).row(
        ikb("▪️ Modifier la description", data=f"position_edit_desc:{position_id}:{category_id}:{remover}"),
        ikb("▪️ Modifier la photo", data=f"position_edit_photo:{position_id}:{category_id}:{remover}"),
    ).row(
        ikb("▪️ Ajouter des produits", data=f"item_add_position_open:{position_id}:{category_id}"),
        ikb("▪️ Exporter les produits", data=f"position_edit_items:{position_id}:{category_id}:{remover}"),
    ).row(
        ikb("▪️ Vider les produits", data=f"position_edit_clear:{position_id}:{category_id}:{remover}"),
        ikb("▪️ Supprimer un produit", data=f"item_delete_swipe:{position_id}:{category_id}:0"),
    ).row(
        ikb("▪️ Supprimer la position", data=f"position_edit_delete:{position_id}:{category_id}:{remover}"),
    ).row(
        ikb("🔙 Retour", data=f"position_edit_swipe:{category_id}:{remover}"),
        ikb("▪️ Actualiser", data=f"position_edit_open:{position_id}:{category_id}:{remover}"),
    )

    return keyboard.as_markup()


# Confirmation de la suppression de la position
def position_edit_delete_finl(position_id, category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Oui, supprimer", data=f"position_edit_delete_confirm:{position_id}:{category_id}:{remover}"),
        ikb("❌ Non, annuler", data=f"position_edit_open:{position_id}:{category_id}:{remover}")
    )

    return keyboard.as_markup()


# Confirmation du vidage de la position
def position_edit_clear_finl(position_id, category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Oui, vider", data=f"position_edit_clear_confirm:{position_id}:{category_id}:{remover}"),
        ikb("❌ Non, annuler", data=f"position_edit_open:{position_id}:{category_id}:{remover}")
    )

    return keyboard.as_markup()


# Annulation de la modification de la position et retour
def position_edit_cancel_finl(position_id, category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("❌ Annuler", data=f"position_edit_open:{position_id}:{category_id}:{remover}"),
    )

    return keyboard.as_markup()


##################################### PRODUITS ###################################
# Annulation de la modification de la position et retour
def item_add_finish_finl(position_id: Union[int, str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Terminer le téléchargement", data=f"item_add_position_finish:{position_id}"),
    )

    return keyboard.as_markup()


# Suppression du produit
def item_delete_finl(item_id, position_id, category_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("▪️ Supprimer le produit", data=f"item_delete_confirm:{item_id}"),
    ).row(
        ikb("🔙 Retour", data=f"item_delete_swipe:{position_id}:{category_id}:0"),
    )

    return keyboard.as_markup()


############################### SUPPRESSION DES SECTIONS ##############################
# Choix de la section à supprimer
def products_removes_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🗃 Supprimer toutes les catégories", data=f"prod_removes_categories"),
    ).row(
        ikb("📁 Supprimer toutes les positions", data=f"prod_removes_positions"),
    ).row(
        ikb("🎁 Supprimer tous les produits", data=f"prod_removes_items"),
    )

    return keyboard.as_markup()


# Suppression de toutes les catégories
def products_removes_categories_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Oui, tout supprimer", data="prod_removes_categories_confirm"),
        ikb("❌ Non, annuler", data="prod_removes_return")
    )

    return keyboard.as_markup()


# Suppression de toutes les positions
def products_removes_positions_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Oui, tout supprimer", data="prod_removes_positions_confirm"),
        ikb("❌ Non, annuler", data="prod_removes_return")
    )

    return keyboard.as_markup()


# Suppression de tous les produits
def products_removes_items_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Oui, tout supprimer", data="prod_removes_items_confirm"),
        ikb("❌ Non, annuler", data="prod_removes_return")
    )

    return keyboard.as_markup()
