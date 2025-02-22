# - *- coding: utf- 8 - *-
import sqlite3

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.database.db_helper import dict_factory, update_format

# Modèle de la table
class SettingsModel(BaseModel):
    status_work: str
    status_refill: str
    status_buy: str
    misc_faq: str
    misc_support: str
    misc_bot: str
    misc_item_hide: str
    misc_profit_day: int
    misc_profit_week: int
    misc_profit_month: int

# Gestion des paramètres
class Settingsx:
    storage_name = "storage_settings"

    # Récupération d'un enregistrement
    @staticmethod
    def get() -> SettingsModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Settingsx.storage_name}"

            return SettingsModel(**con.execute(sql).fetchone())

    # Modification d'un enregistrement
    @staticmethod
    def update(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Settingsx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)

            con.execute(sql, parameters)
