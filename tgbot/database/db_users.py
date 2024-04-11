# - *- coding: utf- 8 - *-
import sqlite3

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.database.db_helper import dict_factory, update_format_where, update_format
from tgbot.utils.const_functions import get_unix, ded

# Modèle de la table
class UserModel(BaseModel):
    increment: int
    user_id: int
    user_login: str
    user_name: str
    user_balance: float
    user_refill: float
    user_give: float
    user_unix: int

# Gestion des utilisateurs
class Userx:
    storage_name = "storage_users"

    # Ajout d'un enregistrement
    @staticmethod
    def add(
            user_id: int,
            user_login: str,
            user_name: str,
    ):
        user_balance = 0
        user_refill = 0
        user_give = 0
        user_unix = get_unix()

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(f"""
                    INSERT INTO {Userx.storage_name} (
                        user_id,
                        user_login,
                        user_name,
                        user_balance,
                        user_refill,
                        user_give,
                        user_unix
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """),
                [
                    user_id,
                    user_login,
                    user_name,
                    user_balance,
                    user_refill,
                    user_give,
                    user_unix,
                ],
            )

    # Récupération d'un enregistrement
    @staticmethod
    def get(**kwargs) -> UserModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Userx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = UserModel(**response)

            return response

    # Récupération de plusieurs enregistrements
    @staticmethod
    def gets(**kwargs) -> list[UserModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Userx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [UserModel(**cache_object) for cache_object in response]

            return response

    # Récupération de tous les enregistrements
    @staticmethod
    def get_all() -> list[UserModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Userx.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [UserModel(**cache_object) for cache_object in response]

            return response

    # Modification d'un enregistrement
    @staticmethod
    def update(user_id, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Userx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(user_id)

            con.execute(sql + "WHERE user_id = ?", parameters)

    # Suppression d'un enregistrement
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Userx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Nettoyage de tous les enregistrements
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Userx.storage_name}"

            con.execute(sql)
