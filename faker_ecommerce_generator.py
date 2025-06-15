import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker()

# Configuration
NUM_PRODUCTS = 50
NUM_CATEGORIES = 10
NUM_CUSTOMERS = 100
NUM_ORDERS = 200
MAX_ORDER_ITEMS = 5

# Output folder
output_dir = Path("faked_ecommerce_data")
output_dir.mkdir(parents=True, exist_ok=True)

# Generate categories
categories = []
for i in range(1, NUM_CATEGORIES + 1):
    categories.append({
        "category_id": i,
        "name": fake.word().capitalize(),
        "parent_category_id": random.choice([None] + list(range(1, i))) if i > 1 else None
    })

# Generate products
products = []
for i in range(1, NUM_PRODUCTS + 1):
    products.append({
        "product_id": i,
        "name": fake.word().capitalize(),
        "description": fake.sentence(),
        "price": round(random.uniform(5, 500), 2),
        "availability": random.choice([True, False]),
        "category_id": random.randint(1, NUM_CATEGORIES)
    })

# Generate customers
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "customer_id": i,
        "full_name": fake.name(),
        "email": fake.email(),
        "street": fake.street_address(),
        "city": fake.city(),
        "region": fake.state(),
        "postal_code": fake.postcode(),
        "country": fake.country(),
        "registration_date": fake.date_between(start_date='-2y', end_date='today')
    })

# Generate orders
orders = []
for i in range(1, NUM_ORDERS + 1):
    customer = random.choice(customers)
    orders.append({
        "order_id": i,
        "customer_id": customer["customer_id"],
        "order_date": fake.date_between(start_date=customer["registration_date"], end_date='today'),
        "status": random.choice(["pending", "shipped", "cancelled", "delivered"])
    })

# Generate order items
order_items = []
order_item_id = 1
for order in orders:
    for _ in range(random.randint(1, MAX_ORDER_ITEMS)):
        product = random.choice(products)
        quantity = random.randint(1, 10)
        order_items.append({
            "order_item_id": order_item_id,
            "order_id": order["order_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": product["price"]
        })
        order_item_id += 1

# Generate transactions
transactions = []
for order in orders:
    transactions.append({
        "transaction_id": order["order_id"],
        "order_id": order["order_id"],
        "transaction_date": order["order_date"],
        "payment_method": random.choice(["card", "paypal", "bank_transfer"]),
        "amount": sum(oi["quantity"] * oi["unit_price"] for oi in order_items if oi["order_id"] == order["order_id"])
    })

# Save to CSV inside data folder
pd.DataFrame(categories).to_csv(output_dir / "categories.csv", index=False)
pd.DataFrame(products).to_csv(output_dir / "products.csv", index=False)
pd.DataFrame(customers).to_csv(output_dir / "customers.csv", index=False)
pd.DataFrame(orders).to_csv(output_dir / "orders.csv", index=False)
pd.DataFrame(order_items).to_csv(output_dir / "order_items.csv", index=False)
pd.DataFrame(transactions).to_csv(output_dir / "transactions.csv", index=False)

print("✅ Fake e-commerce data generated successfully to '1_data_modeling_ecommerce/data/'")
