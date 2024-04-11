# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.database.db_payments import Paymentsx
from tgbot.database.db_settings import Settingsx
from tgbot.utils.const_functions import ikb

################################################################################
#################################### DIVERS ####################################
# Suppression du message
def close_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("❌ Fermer", data="close_this"),
    )

    return keyboard.as_markup()


# Confirmation de l'envoi d'un mail
def mail_confirm_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Envoyer", data="confirm_mail:yes"),
        ikb("❌ Annuler", data="confirm_mail:not"),
    )

    return keyboard.as_markup()


# Recherche de profil utilisateur
def profile_search_finl(user_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("💰 Modifier le solde", data=f"admin_user_balance_set:{user_id}"),
        ikb("💰 Créditer un solde", data=f"admin_user_balance_add:{user_id}"),
    ).row(
        ikb("🎁 Achats", data=f"admin_user_purchases:{user_id}"),
        ikb("💌 Envoyer un SMS", data=f"admin_user_message:{user_id}"),
    ).row(
        ikb("🔄 Actualiser", data=f"admin_user_refresh:{user_id}"),
    )

    return keyboard.as_markup()


# Retour au profil utilisateur
def profile_search_return_finl(user_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("❌ Annuler", data=f"admin_user_refresh:{user_id}"),
    )

    return keyboard.as_markup()


################################################################################
############################## SYSTÈMES DE PAIEMENT ###############################
# Méthodes de paiement
def payment_method_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_payments = Paymentsx.get()

    status_qiwi_kb = ikb("✅", data="payment_method:QIWI:False")
    status_yoomoney_kb = ikb("✅", data="payment_method:Yoomoney:False")

    if get_payments.way_qiwi == "False":
        status_qiwi_kb = ikb("❌", data="payment_method:QIWI:True")
    if get_payments.way_yoomoney == "False":
        status_yoomoney_kb = ikb("❌", data="payment_method:Yoomoney:True")

    keyboard.row(
        ikb("🥝 QIWI", url="https://vk.cc/csUUYy"), status_qiwi_kb,
    ).row(
        ikb("🔮 YooMoney", url="https://vk.cc/csUUXt"), status_yoomoney_kb,
    )

    return keyboard.as_markup()


# Gestion de YooMoney
def payment_yoomoney_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🔮 Solde 💰", data="payment_yoomoney_balance"),
    ).row(
        ikb("🔮 Vérifier ♻️", data="payment_yoomoney_check"),
    ).row(
        ikb("🔮 Modifier 🖍", data="payment_yoomoney_edit"),
    )

    return keyboard.as_markup()


# Gestion de QIWI
def payment_qiwi_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🥝 Solde 💰", data="payment_qiwi_balance"),
    ).row(
        ikb("🥝 Vérifier ♻️", data="payment_qiwi_check"),
    ).row(
        ikb("🥝 Modifier 🖍", data="payment_qiwi_edit"),
    )

    return keyboard.as_markup()


################################################################################
################################## PARAMÈTRES ###################################
# Boutons des paramètres
def settings_open_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_settings = Settingsx.get()

    # Support
    if get_settings.misc_support == "None":
        support_kb = ikb("Non défini ❌", data="settings_edit_support")
    else:
        support_kb = ikb(f"@{get_settings.misc_support} ✅", data="settings_edit_support")

    # FAQ
    if get_settings.misc_faq == "None":
        faq_kb = ikb("Non défini ❌", data="settings_edit_faq")
    else:
        faq_kb = ikb(f"{get_settings.misc_faq[:15]}... ✅", data="settings_edit_faq")

    if get_settings.misc_item_hide == "True":
        item_hide_kb = ikb("Cachés", data="settings_edit_item_hide:False")
    else:
        item_hide_kb = ikb("Affichés", data="settings_edit_item_hide:True")

    keyboard.row(
        ikb("❔ FAQ", data="..."), faq_kb,
    ).row(
        ikb("☎️ Support", data="..."), support_kb,
    ).row(
        ikb("🎁 Positions sans produits", data="..."), item_hide_kb,
    )

    return keyboard.as_markup()


# Interrupteurs
def turn_open_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_settings = Settingsx.get()

    status_work_kb = ikb("Activés ✅", data="turn_work:False")
    status_buy_kb = ikb("Activés ✅", data="turn_buy:False")
    status_refill_kb = ikb("Activés ✅", data="turn_pay:False")

    if get_settings.status_buy == "False":
        status_buy_kb = ikb("Désactivés ❌", data="turn_buy:True")
    if get_settings.status_work == "False":
        status_work_kb = ikb("Désactivés ❌", data="turn_work:True")
    if get_settings.status_refill == "False":
        status_refill_kb = ikb("Désactivés ❌", data="turn_pay:True")

    keyboard.row(
        ikb("⛔ Travaux techniques", data="..."), status_work_kb,
    ).row(
        ikb("💰 Recharges", data="..."), status_refill_kb,
    ).row(
        ikb("🎁 Achats", data="..."), status_buy_kb,
    )

    return keyboard.as_markup()
