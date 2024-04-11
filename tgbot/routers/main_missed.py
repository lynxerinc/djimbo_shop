# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, Message

from tgbot.utils.const_functions import del_message, ded
from tgbot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)


# Callback pour la suppression du message
@router.callback_query(F.data == "close_this")
async def main_missed_callback_close(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    # Supprimer le message à l'origine du callback
    await del_message(call.message)


# Callback pour gérer un bouton avec une action définie par "..."
@router.callback_query(F.data == "...")
async def main_missed_callback_answer(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    # Répondre au callback sans aucun message visible par l'utilisateur
    await call.answer(cache_time=60)


# Traitement de tous les callbacks qui ont perdu leur état après le redémarrage du script
@router.callback_query()
async def main_missed_callback(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS):
    # Informer l'utilisateur que le bouton n'est plus valide et qu'il doit répéter l'action
    await call.answer("❗️ Ce bouton n'est plus valide. Veuillez répéter votre action.", True)


# Gestion de toutes les commandes inconnues
@router.message()
async def main_missed_message(message: Message, bot: Bot, state: FSM, arSession: ARS):
    # Répondre à l'utilisateur avec un message indiquant que la commande est inconnue
    await message.answer(
        ded(f"""
            ♦️ Commande inconnue.
            ♦️ Veuillez taper /start
        """),
    )
