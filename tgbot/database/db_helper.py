# - *- coding: utf- 8 - *-
import sqlite3

from tgbot.data.config import PATH_DATABASE
from tgbot.utils.const_functions import get_unix, ded

# Conversion de la liste obtenue en dictionnaire
def dict_factory(cursor, row) -> dict:
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict

# Formatage de la requête sans arguments
def update_format(sql, parameters: dict) -> tuple[str, list]:
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql += f" {values}"

    return sql, list(parameters.values())

# Formatage de la requête avec arguments
def update_format_where(sql, parameters: dict) -> tuple[str, list]:
    sql += " WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())

################################################################################
# Création de toutes les tables pour la base de données
def create_dbx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory

        ############################################################
        # Création de la table de stockage - utilisateurs
        if len(con.execute("PRAGMA table_info(storage_users)").fetchall()) == 8:
            print("Base de données trouvée (1/8)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_users(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        user_login TEXT,
                        user_name TEXT,
                        user_balance REAL,
                        user_refill REAL,
                        user_give REAL,
                        user_unix INTEGER
                    )
                """)
            )
            print("Base de données non trouvée (1/8) | Création...")

        # Création de la table de stockage - paramètres
        if len(con.execute("PRAGMA table_info(storage_settings)").fetchall()) == 10:
            print("Base de données trouvée (2/8)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_settings(
                        status_work TEXT,
                        status_refill TEXT,
                        status_buy TEXT,
                        misc_faq TEXT,
                        misc_support TEXT,
                        misc_bot TEXT,
                        misc_item_hide TEXT,
                        misc_profit_day INTEGER,
                        misc_profit_week INTEGER,
                        misc_profit_month INTEGER
                    )
                """)
            )

            con.execute(
                ded(f"""
                    INSERT INTO storage_settings(
                        status_work,
                        status_refill,
                        status_buy,
                        misc_faq,
                        misc_support,
                        misc_bot,
                        misc_item_hide,
                        misc_profit_day,
                        misc_profit_week,
                        misc_profit_month
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """),
                [
                    'True',
                    'False',
                    'False',
                    'None',
                    'None',
                    'None',
                    'False',
                    get_unix(),
                    get_unix(),
                    get_unix(),
                ]
            )
            print("Base de données non trouvée (2/8) | Création...")

        ############################################################
        # Création de la table de stockage - données des systèmes de paiement
        if len(con.execute("PRAGMA table_info(storage_payment)").fetchall()) == 5:
            print("Base de données trouvée (3/8)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_payment(
                        qiwi_login TEXT,
                        qiwi_token TEXT,
                        yoomoney_token TEXT,
                        way_qiwi TEXT,
                        way_yoomoney TEXT
                    )
                """)
            )

            con.execute(
                ded(f"""
                    INSERT INTO storage_payment(
                        qiwi_login,
                        qiwi_token,
                        yoomoney_token,
                        way_qiwi,
                        way_yoomoney
                    ) 
                    VALUES (?, ?, ?, ?, ?)
                """),
                [
                    'None',
                    'None',
                    'None',
                    'False',
                    'False',
                ]
            )
            print("Base de données non trouvée (3/8) | Création...")

        ############################################################
        # Création de la table de stockage - recharges des utilisateurs
        if len(con.execute("PRAGMA table_info(storage_refill)").fetchall()) == 7:
            print("Base de données trouvée (4/8)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_refill(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        refill_comment TEXT,
                        refill_amount REAL,
                        refill_receipt TEXT,
                        refill_method TEXT,
                        refill_unix INTEGER
                    )
                """)
            )
            print("Base de données non trouvée (4/8) | Création...")

        ############################################################
        # Création de la table de stockage - catégories
        if len(con.execute("PRAGMA table_info(storage_category)").fetchall()) == 4:
            print("Base de données trouvée (5/8)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_category(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        category_id INTEGER,
                        category_name TEXT,
                        category_unix INTEGER
                    )
                """)
            )
            print("Base de données non trouvée (5/8) | Création...")

        ############################################################
        # Création de la table de stockage - positions
        if len(con.execute("PRAGMA table_info(storage_position)").fetchall()) == 8:
            print("Base de données trouvée (6/8)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_position(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        category_id INTEGER,
                        position_id INTEGER,
                        position_name TEXT,
                        position_price REAL,
                        position_desc TEXT,
                        position_photo TEXT,
                        position_unix INTEGER
                    )
                """)
            )
            print("Base de données non trouvée (6/8) | Création...")

        ############################################################
        # Création de la table de stockage - articles
        if len(con.execute("PRAGMA table_info(storage_item)").fetchall()) == 7:
            print("Base de données trouvée (7/8)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_item(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        category_id INTEGER,
                        position_id INTEGER,
                        item_id INTEGER,
                        item_unix INTEGER,
                        item_data TEXT
                    )
                """)
            )
            print("Base de données non trouvée (7/8) | Création...")

        ############################################################
        # Création de la table de stockage - achats
        if len(con.execute("PRAGMA table_info(storage_purchases)").fetchall()) == 14:
            print("Base de données trouvée (8/8)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_purchases(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        user_balance_before REAL,
                        user_balance_after REAL,
                        purchase_receipt TEXT,
                        purchase_data TEXT,
                        purchase_count INTEGER,
                        purchase_price REAL,
                        purchase_price_one REAL,
                        purchase_position_id INTEGER,
                        purchase_position_name TEXT,
                        purchase_category_id INTEGER,
                        purchase_category_name TEXT,
                        purchase_unix INTEGER
                    )
                """)
            )
            print("Base de données non trouvée (8/8) | Création...")
