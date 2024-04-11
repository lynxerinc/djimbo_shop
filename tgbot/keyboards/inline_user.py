# - *- coding: utf- 8 - *-
from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.database.db_payments import Paymentsx
from tgbot.utils.const_functions import ikb


################################################################################
#################################### DIVERS ####################################
# Accès à son profil
def user_profile_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💰 Recharger", data="user_refill"),
        ikb("🎁 Mes achats", data="user_purchases"),
    )

    return keyboard.as_markup()


# Lien vers le support
def user_support_finl(support_login: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💌 Contacter le support", url=f"https://t.me/{support_login}"),
    )

    return keyboard.as_markup()


################################################################################
################################### PAIEMENTS ####################################
# Choix des méthodes de recharge
def refill_method_finl() -> Union[InlineKeyboardMarkup, None]:
    keyboard = InlineKeyboardBuilder()

    get_payments = Paymentsx.get()

    if get_payments.way_qiwi == "True":
        keyboard.row(ikb("🥝 QIWI", data="user_refill_method:QIWI"))
    if get_payments.way_yoomoney == "True":
        keyboard.row(ikb("🔮 YooMoney", data="user_refill_method:Yoomoney"))

    keyboard.row(ikb("🔙 Retour", data="user_profile"))

    return keyboard.as_markup()


# Vérification du paiement
def refill_bill_finl(pay_link: str, pay_receipt: Union[str, int], pay_way: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🌀 Payer maintenant", url=pay_link),
    ).row(
        ikb("🔄 Vérifier le paiement", data=f"Pay:{pay_way}:{pay_receipt}"),
    )

    return keyboard.as_markup()


################################################################################
#################################### PRODUITS ####################################
# Ouverture d'une position pour visualisation
def products_open_finl(position_id, category_id, remover) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💰 Acheter un produit", data=f"buy_item_open:{position_id}:{remover}"),
    ).row(
        ikb("🔙 Retour", data=f"buy_category_open:{category_id}:{remover}"),
    )

    return keyboard.as_markup()


# Confirmation de l'achat d'un produit
def products_confirm_finl(position_id, category_id, get_count) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Confirmer", data=f"buy_item_confirm:{position_id}:{get_count}"),
        ikb("❌ Annuler", data=f"buy_position_open:{position_id}:0"),
    )

    return keyboard.as_markup()


# Retour à la position en cas d'annulation de saisie
def products_return_finl(position_id, category_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🔙 Retour", data=f"buy_position_open:{position_id}:0"),
    )

    return keyboard.as_markup()
