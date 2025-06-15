import sqlite3
from pathlib import Path
import pandas as pd

def run_sql_script(conn, sql_path):
    sql = sql_path.read_text()
    conn.executescript(sql)

def import_csv_to_db(conn, table_name, csv_path):
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Imported {len(df)} rows into {table_name}")

def main():
    BASE_DIR = Path(__file__).parent.resolve()
    DATA_DIR = BASE_DIR / 'faked_ecommerce_data'
    DB_PATH = BASE_DIR / 'fake_ecommerce.db'

    with sqlite3.connect(DB_PATH) as conn:
        # 1. Vytvorenie základných tabuliek podľa sql_schema.sql
        print("Creating base tables...")
        run_sql_script(conn, BASE_DIR / 'sql_schema.sql')

        # 2. Import CSV dát do staging tabuliek
        csv_table_map = {
            'categories': 'categories.csv',
            'products': 'products.csv',
            'customers': 'customers.csv',
            'orders': 'orders.csv',
            'order_items': 'order_items.csv',
            'transactions': 'transactions.csv'
        }
        for table, csv_file in csv_table_map.items():
            csv_path = DATA_DIR / csv_file
            import_csv_to_db(conn, table, csv_path)

        # 3. Vytvorenie star schema podľa build_star_schema.sql
        print("Building star schema...")
        run_sql_script(conn, BASE_DIR / 'build_star_schema.sql')

    print("All done!")

if __name__ == "__main__":
    main()
