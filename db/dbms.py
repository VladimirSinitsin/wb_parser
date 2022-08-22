import sqlite3

from pathlib import Path

from config import ROOTPATH
from config import DEBUG


# Debugging.
if DEBUG and Path.joinpath(ROOTPATH, "db/products.db").exists():
    Path.joinpath(ROOTPATH, "db/products.db").unlink()

# Connect to DB.
db_path = Path.joinpath(ROOTPATH, "db/products.db")
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()


# Check if the database was not created.
cursor.execute("SELECT name FROM sqlite_master "
               "WHERE type='table' AND name='Products'")
table_exists = cursor.fetchall()
if not table_exists:
    with open(Path.joinpath(ROOTPATH, "db/createdb.sql"), "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def insert(column_values: dict) -> None:
    """
    Insert values in DB.
    :param column_values: dictionary with columns(keys) and values.
    """
    columns = ", ".join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(f"INSERT INTO Products ({columns}) VALUES ({placeholders})", values)
    conn.commit()


def select_all_products_data() -> list:
    """ Get all products data from DB. """
    cursor.execute(f"SELECT * FROM Products")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {"id": row[0],
                    "name": row[1],
                    "price": row[2]}
        result.append(dict_row)
    return result
