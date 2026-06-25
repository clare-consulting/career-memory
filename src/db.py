import sqlite3
from pathlib import Path

DB_PATH = Path("career_memory.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    schema_path = Path("database/schema.sql")

    with get_connection() as conn:
        conn.executescript(schema_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    initialize_database()
    print(f"Initialized database at {DB_PATH}")