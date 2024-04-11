# - *- coding: utf- 8 - *-
import sqlite3

from pydantic import BaseModel

from tgbot.data.config import PATH_DATABASE
from tgbot.database.db_helper import dict_factory, update_format_where, update_format
from tgbot.utils.const_functions import ded, get_unix

# Modèle de table
class CategoryModel(BaseModel):
    increment: int
    category_id: int
    category_name: str
    category_unix: int

# Gestion des catégories
class Categoryx:
    storage_name = "storage_category"

    # Ajout d'une entrée
    @staticmethod
    def add(
            category_id: int,
            category_name: str,
    ):
        category_unix = get_unix()

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(f"""
                    INSERT INTO {Categoryx.storage_name} (
                        category_id,
                        category_name,
                        category_unix
                    ) VALUES (?, ?, ?)
                """),
                [
                    category_id,
                    category_name,
                    category_unix,
                ],
            )

    # Récupération d'une entrée
    @staticmethod
    def get(**kwargs) -> CategoryModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Categoryx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = CategoryModel(**response)

            return response

    # Récupération de plusieurs entrées
    @staticmethod
    def gets(**kwargs) -> list[CategoryModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Categoryx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [CategoryModel(**cache_object) for cache_object in response]

            return response

    # Récupération de toutes les entrées
    @staticmethod
    def get_all() -> list[CategoryModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Categoryx.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [CategoryModel(**cache_object) for cache_object in response]

            return response

    # Modification d'une entrée
    @staticmethod
    def update(category_id, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Categoryx.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(category_id)

            con.execute(sql + "WHERE category_id = ?", parameters)

    # Suppression d'une entrée
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Categoryx.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Nettoyage de toutes les entrées
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Categoryx.storage_name}"

            con.execute(sql)
