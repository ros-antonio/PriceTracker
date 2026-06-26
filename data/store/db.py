import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional


DB_PATH = Path(os.getenv("PRICE_TRACKER_DB", "data/prices.db"))


def _get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with _get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT NOT NULL,
                link TEXT NOT NULL,
                store TEXT NOT NULL,
                price REAL NOT NULL,
                stock TEXT,
                checked_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_prices_product ON prices(tag, link, id)"
        )


def get_last_price(tag: str, link: str) -> Optional[float]:
    with _get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT price
            FROM prices
            WHERE tag = ? AND link = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (tag, link),
        )
        row = cursor.fetchone()
        return float(row[0]) if row else None


def insert_price(tag: str, link: str, store: str, price: float, stock: Optional[str]) -> None:
    with _get_connection() as conn:
        conn.execute(
            """
            INSERT INTO prices (tag, link, store, price, stock, checked_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (tag, link, store, price, stock, datetime.now().isoformat(timespec="seconds")),
        )
