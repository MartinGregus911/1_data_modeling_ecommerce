import sqlite3
from pathlib import Path


def run_sql_script(conn, sql_file):
    sql = sql_file.read_text()
    conn.executescript(sql)


BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "fake_ecommerce.db"

with sqlite3.connect(DB_PATH) as conn:
    # 1. Vytvorenie základnej relačnej štruktúry (sql_schema.sql)
    run_sql_script(conn, BASE_DIR / "sql_schema.sql")

    # 2. Import CSV dát do staging tabuliek (tu by si zavolal kód na import CSV)
    # Napr. generate_fake_ecommerce_db.py alebo inline import

    # 3. Vytvorenie star schema (build_star_schema.sql)
    run_sql_script(conn, BASE_DIR / "build_star_schema.sql")
