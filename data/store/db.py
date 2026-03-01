import os
import sqlite3
from typing import Optional

DB_DIR = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(DB_DIR, "prices.db")


def _get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    os.makedirs(DB_DIR, exist_ok=True)
    conn = _get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prices (
                tag   TEXT NOT NULL,
                priceFound INTEGER NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def get_last_price(tag: str) -> Optional[int]:
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT priceFound FROM prices WHERE tag = ? ORDER BY rowid DESC LIMIT 1",
            (tag,),
        )
        row = cursor.fetchone()
        return row[0] if row else None
    finally:
        conn.close()


def insert_price(tag: str, price: int) -> None:
    conn = _get_connection()
    try:
        conn.execute("INSERT INTO prices (tag, priceFound) VALUES (?, ?)", (tag, price))
        conn.commit()
    finally:
        conn.close()
