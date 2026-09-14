from pathlib import Path
import sqlite3

base = Path(__file__).resolve().parent
db_path = base / "jlpt_learning.db"

with sqlite3.connect(db_path) as connection:
    connection.executescript((base / "schema.sql").read_text(encoding="utf-8"))
    connection.executescript((base / "seed_2026_08_26.sql").read_text(encoding="utf-8"))
    connection.commit()

print(db_path)

