import os
import sqlite3

from heritage.database import DEFAULT_DB_PATH, Database
from heritage.menu import HeritageCLI, choose_role
from heritage.services import HeritageService


def main():
    db_path = os.environ.get("HERITAGE_DB", DEFAULT_DB_PATH)
    try:
        db = Database(db_path)
    except sqlite3.Error as exc:
        print(f"Could not open database: {exc}")
        return
    try:
        role = choose_role()
        service = HeritageService(db, role)
        HeritageCLI(service).run()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting. Goodbye!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
