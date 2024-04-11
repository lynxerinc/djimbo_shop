# - *- coding: utf- 8 - *-
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from tgbot.data.config import get_admins
from tgbot.utils.const_functions import rkb


# Boutons du menu principal
def menu_frep(user_id) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🎁 Acheter"), rkb("👤 Profil"), rkb("🧮 Disponibilité des produits"),
    ).row(
        rkb("☎️ Support"), rkb("❔ FAQ")
    )

    if user_id in get_admins():
        keyboard.row(
            rkb("🎁 Gestion des produits"), rkb("📊 Statistiques"),
        ).row(
            rkb("⚙️ Paramètres"), rkb("🔆 Fonctions générales"), rkb("🔑 Systèmes de paiement"),
        )

    return keyboard.as_markup(resize_keyboard=True)


# Boutons des systèmes de paiement
def payments_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🔮 YooMoney"), rkb("🥝 QIWI"),
    ).row(
        rkb("🔙 Menu principal"), rkb("🖲 Méthodes de recharge")
    )

    return keyboard.as_markup(resize_keyboard=True)


# Boutons des fonctions générales
def functions_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🔍 Recherche"), rkb("📢 Mailing"),
    ).row(
        rkb("🔙 Menu principal")
    )

    return keyboard.as_markup(resize_keyboard=True)


# Boutons des paramètres
def settings_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("🖍 Modifier les informations"), rkb("🕹 Interrupteurs"),
    ).row(
        rkb("🔙 Menu principal")
    )

    return keyboard.as_markup(resize_keyboard=True)


# Boutons de gestion des produits
def items_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        rkb("📁 Créer une position ➕"), rkb("🗃 Créer une catégorie ➕"),
    ).row(
        rkb("📁 Modifier une position 🖍"), rkb("🗃 Modifier une catégorie 🖍")
    ).row(
        rkb("🔙 Menu principal"), rkb("🎁 Ajouter des produits ➕"), rkb("❌ Suppression")
    )

    return keyboard.as_markup(resize_keyboard=True)
