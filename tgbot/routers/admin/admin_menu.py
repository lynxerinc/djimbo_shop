# - *- coding: utf- 8 - *-
import os

import aiofiles
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from tgbot.data.config import PATH_LOGS, PATH_DATABASE
from tgbot.keyboards.reply_main import payments_frep, settings_frep, functions_frep, items_frep
from tgbot.utils.const_functions import get_date
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import get_statistics

router = Router(name=__name__)


# Systèmes de paiement
@router.message(F.text == "🔑 Systèmes de paiement")
async def admin_payments(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🔑 Configuration des systèmes de paiement.</b>",
        reply_markup=payments_frep(),
    )


# Paramètres du bot
@router.message(F.text == "⚙️ Paramètres")
async def admin_settings(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>⚙️ Paramètres principaux du bot.</b>",
        reply_markup=settings_frep(),
    )


# Fonctions générales
@router.message(F.text == "🔆 Fonctions générales")
async def admin_functions(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🔆 Sélectionnez la fonction souhaitée.</b>",
        reply_markup=functions_frep(),
    )


# Gestion des produits
@router.message(F.text == "🎁 Gestion des produits")
async def admin_products(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(
        "<b>🎁 Édition des produits.</b>",
        reply_markup=items_frep(),
    )


# Statistiques du bot
@router.message(F.text == "📊 Statistiques")
async def admin_statistics(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer(get_statistics())


# Récupération de la base de données
@router.message(Command(commands=['db', 'database']))
async def admin_database(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    await message.answer_document(
        FSInputFile(PATH_DATABASE),
        caption=f"<b>📦 #SAUVEGARDE | <code>{get_date()}</code></b>",
    )


# Récupération des journaux (logs)
@router.message(Command(commands=['log', 'logs']))
async def admin_log(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    media_group = MediaGroupBuilder(
        caption=f"<b>🖨 #JOURNAUX | <code>{get_date()}</code></b>",
    )

    if os.path.isfile(PATH_LOGS):
        media_group.add_document(media=FSInputFile(PATH_LOGS))

    if os.path.isfile("tgbot/data/sv_log_err.log"):
        media_group.add_document(media=FSInputFile("tgbot/data/sv_log_err.log"))

    if os.path.isfile("tgbot/data/sv_log_out.log"):
        media_group.add_document(media=FSInputFile("tgbot/data/sv_log_out.log"))

    await message.answer_media_group(media=media_group.build())


# Nettoyage des journaux (logs)
@router.message(Command(commands=['clear_log', 'clear_logs', 'log_clear', 'logs_clear']))
async def admin_log_clear(message: Message, bot: Bot, state: FSM, arSession: ARS):
    await state.clear()

    if os.path.isfile(PATH_LOGS):
        async with aiofiles.open(PATH_LOGS, "w") as file:
            await file.write(f"{get_date()} | LES JOURNAUX ONT ÉTÉ NETTOYÉS")

    if os.path.isfile("tgbot/data/sv_log_err.log"):
        async with aiofiles.open("tgbot/data/sv_log_err.log", "w") as file:
            await file.write(f"{get_date()} | LES JOURNAUX D'ERREURS ONT ÉTÉ NETTOYÉS")

    if os.path.isfile("tgbot/data/sv_log_out.log"):
        async with aiofiles.open("tgbot/data/sv_log_out.log", "w") as file:
            await file.write(f"{get_date()} | LES JOURNAUX DE SORTIE ONT ÉTÉ NETTOYÉS")

    await message.answer("<b>🖨 Les journaux ont été nettoyés avec succès</b>")
