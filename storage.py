import os
import sqlite3
import time

DB_PATH = os.getenv("DB_PATH", "/data/seen.sqlite3")

SCHEMA = """
CREATE TABLE IF NOT EXISTS seen_items (
key TEXT PRIMARY KEY,
title TEXT,
url TEXT,
site TEXT,
first_seen INTEGER
);
"""


def init_db():
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
with sqlite3.connect(DB_PATH) as conn:
conn.execute(SCHEMA)


def has_seen(key: str) -> bool:
with sqlite3.connect(DB_PATH) as conn:
cur = conn.execute("SELECT 1 FROM seen_items WHERE key = ?", (key,))
return cur.fetchone() is not None


def mark_seen(key: str, title: str, url: str, site: str):
with sqlite3.connect(DB_PATH) as conn:
conn.execute(
"INSERT OR IGNORE INTO seen_items (key, title, url, site, first_seen) VALUES (?,?,?,?,?)",
(key, title, url, site, int(time.time())),
)
