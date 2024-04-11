# - *- coding: utf- 8 - *-
import asyncio
import os
import sys

import colorama
from aiogram import Dispatcher, Bot

from tgbot.data.config import get_admins, BOT_TOKEN, BOT_SCHEDULER
from tgbot.database.db_helper import create_dbx
from tgbot.middlewares import register_all_middlwares
from tgbot.routers import register_all_routers
from tgbot.services.api_session import AsyncRequestSession
from tgbot.utils.misc.bot_commands import set_commands
from tgbot.utils.misc.bot_logging import bot_logger
from tgbot.utils.misc.bot_models import ARS
from tgbot.utils.misc_functions import (check_update, check_bot_username, startup_notify, update_profit_day,
                                        update_profit_week, autobackup_admin, check_mail, update_profit_month,
                                        autosettings_unix)

colorama.init()

# Démarrage des planificateurs
async def scheduler_start(bot: Bot, arSession: ARS):
    BOT_SCHEDULER.add_job(update_profit_month, trigger="cron", day=1, hour=00, minute=00, second=5)
    BOT_SCHEDULER.add_job(update_profit_week, trigger="cron", day_of_week="mon", hour=00, minute=00, second=10)
    BOT_SCHEDULER.add_job(update_profit_day, trigger="cron", hour=00, minute=00, second=15, args=(bot,))
    BOT_SCHEDULER.add_job(autobackup_admin, trigger="cron", hour=00, args=(bot,))
    BOT_SCHEDULER.add_job(check_update, trigger="cron", hour=00, args=(bot, arSession,))
    BOT_SCHEDULER.add_job(check_mail, trigger="cron", hour=12, args=(bot, arSession,))

# Démarrage du bot et des fonctions de base
async def main():
    BOT_SCHEDULER.start()  # Démarrage du Planificateur
    dp = Dispatcher()  # Instance du Dispatcheur
    arSession = AsyncRequestSession()  # Pool de session de requêtes asynchrones
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")  # Instance du Bot

    register_all_middlwares(dp)  # Enregistrement de tous les middlewares
    register_all_routers(dp)  # Enregistrement de tous les routeurs

    try:
        await autosettings_unix()  # Configuration automatique de l'heure UNIX dans la DB
        await set_commands(bot)  # Configuration des commandes
        await check_bot_username(bot)  # Vérification du nom d'utilisateur du bot dans la DB
        await check_update(bot, arSession)  # Vérification des mises à jour
        await check_mail(bot, arSession)  # Notification des mises à jour
        await startup_notify(bot, arSession)  # Notifications au démarrage du bot
        await scheduler_start(bot, arSession)  # Connexion des planificateurs

        bot_logger.warning("LE BOT A ÉTÉ DÉMARRÉ")
        print(colorama.Fore.LIGHTYELLOW_EX + f"~~~~~ Le bot a été démarré - @{(await bot.get_me()).username} ~~~~~")
        print(colorama.Fore.LIGHTBLUE_EX + "~~~~~ Développeur TG - @djimbox ~~~~~")
        print(colorama.Fore.RESET)

        if len(get_admins()) == 0: print("***** ENTREZ L'ID DE L'ADMINISTRATEUR DANS settings.ini *****")

        await bot.delete_webhook()
        await bot.get_updates(offset=-1)

        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
            arSession=arSession,
        )
    finally:
        await arSession.close()
        await bot.session.close()

if __name__ == "__main__":
    create_dbx()  # Génération de la DB et des tables

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        bot_logger.warning("Le bot a été arrêté")
    finally:
        if sys.platform.startswith("win"):
            os.system("cls")
        else:
            os.system("clear")
