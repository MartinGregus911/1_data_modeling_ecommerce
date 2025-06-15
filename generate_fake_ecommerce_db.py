import sqlite3
import pandas as pd
from pathlib import Path

# Base folder is the folder where this script is located
BASE_DIR = Path(__file__).parent

# CSV files folder
DATA_DIR = BASE_DIR / "faked_ecommerce_data"

# SQLite DB file directly inside 1_data_modeling_ecommerce (same as BASE_DIR)
DB_PATH = BASE_DIR / "fake_ecommerce.db"

# Mapping staging tables to CSV filenames
csv_map = {
    "staging_categories": "categories.csv",
    "staging_products": "products.csv",
    "staging_customers": "customers.csv",
    "staging_orders": "orders.csv",
    "staging_order_items": "order_items.csv",
    "staging_transactions": "transactions.csv"
}

# Connect to (or create) the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Load CSV files into staging tables
for table_name, csv_file in csv_map.items():
    csv_path = DATA_DIR / csv_file
    print(f"Loading {csv_path} into {table_name}...")
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"Rows in {table_name}: {count}")

conn.commit()
conn.close()
print(f"✅ Database created at: {DB_PATH}")
