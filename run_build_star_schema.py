import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent

DB_PATH = BASE_DIR / "fake_ecommerce.db"
SQL_PATH = BASE_DIR / "build_star_schema.sql"

def run_sql_script(db_path, sql_path):
    with sqlite3.connect(db_path) as conn:
        sql = sql_path.read_text()
        conn.executescript(sql)
        print(f"✅ Executed {sql_path.name} on database {db_path.name}")

if __name__ == "__main__":
    run_sql_script(DB_PATH, SQL_PATH)
