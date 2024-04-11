# - *- coding: utf- 8 - *-
import configparser

from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_CONFIG = configparser.ConfigParser()
BOT_CONFIG.read("settings.ini")

# Instances et configurations
BOT_TOKEN = BOT_CONFIG['settings']['bot_token'].strip().replace(' ', '')  # Token du bot
BOT_TIMEZONE = "Europe/Moscow"  # Fuseau horaire du bot
BOT_SCHEDULER = AsyncIOScheduler(timezone=BOT_TIMEZONE)  # Instance du planificateur
BOT_VERSION = 4.0  # Version du bot

# Chemins vers les fichiers
PATH_DATABASE = "tgbot/data/database.db"  # Chemin vers la base de données
PATH_LOGS = "tgbot/data/logs.log"  # Chemin vers les logs


# Obtention des administrateurs du bot
def get_admins() -> list[int]:
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: admins.remove("")
    while " " in admins: admins.remove(" ")
    while "\r" in admins: admins.remove("\r")
    while "\n" in admins: admins.remove("\n")

    admins = list(map(int, admins))

    return admins


# Obtention de la description
def get_desc() -> str:
    from tgbot.utils.const_functions import ded

    # SI TU SUPPRIMES OU MODIFIES LES LIENS DE DON, DE CHAÎNE OU DU SUJET DU BOT - JE TE CASTRE AMICALEMENT <3

    return ded(f"""
        <b>♻️ Version du Bot : <code>{BOT_VERSION}</code>
        👑 Bot créé par @djimbox
        🍩 Faire un don à l'auteur : <a href='https://yoomoney.ru/to/410012580032553'>Cliquez ici</a>
        🤖 Chaîne du Bot [NOUVELLES | MISES À JOUR] : <a href='https://t.me/DJIMBO_SHOP'>Cliquez ici</a>
        🔗 Lien du sujet : <a href='https://lolz.guru/threads/1888814'>Cliquez ici</a></b>
    """).strip()
