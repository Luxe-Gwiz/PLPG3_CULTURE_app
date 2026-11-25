import sqlite3

DEFAULT_DB_PATH = "heritage.db"

CREATE_TRADITIONS = """
CREATE TABLE IF NOT EXISTS traditions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    community   TEXT NOT NULL,
    description TEXT NOT NULL,
    created_by  TEXT NOT NULL
)
"""

CREATE_EVENTS = """
CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name  TEXT NOT NULL,
    event_date  TEXT NOT NULL,
    location    TEXT NOT NULL,
    created_by  TEXT NOT NULL
)
"""


class Database:
    def __init__(self, path=DEFAULT_DB_PATH):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.conn.execute(CREATE_TRADITIONS)
        self.conn.execute(CREATE_EVENTS)
        self.conn.commit()

    def execute(self, sql, params=()):
        self.conn.execute(sql, params)
        self.conn.commit()

    def fetch_all(self, sql, params=()):
        return self.conn.execute(sql, params).fetchall()

    def fetch_one(self, sql, params=()):
        return self.conn.execute(sql, params).fetchone()

    def close(self):
        self.conn.close()
