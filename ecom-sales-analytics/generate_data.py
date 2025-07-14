import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Constants
NUM_CUSTOMERS = 100
NUM_PRODUCTS = 20
NUM_TRANSACTIONS = 1000

# -----------------------------
# 1. Generate Customers
# -----------------------------
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        'customer_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'location': fake.city(),
        'signup_date': fake.date_between(start_date='-2y', end_date='-1d')
    })

df_customers = pd.DataFrame(customers)

# -----------------------------
# 2. Generate Products
# -----------------------------
categories = ['Electronics', 'Clothing', 'Books', 'Beauty', 'Sports']
products = []
for i in range(1, NUM_PRODUCTS + 1):
    products.append({
        'product_id': i,
        'name': f'{random.choice(["Smart", "Eco", "Max", "Ultra"])} Product-{i}',
        'category': random.choice(categories),
        'price': round(random.uniform(10.0, 1000.0), 2)
    })

df_products = pd.DataFrame(products)

# -----------------------------
# 3. Generate Sales
# -----------------------------
sales = []
for i in range(1, NUM_TRANSACTIONS + 1):
    cust = random.choice(customers)
    prod = random.choice(products)
    quantity = random.randint(1, 5)
    order_date = fake.date_between(start_date='-6M', end_date='today')
    
    sales.append({
        'transaction_id': i,
        'customer_id': cust['customer_id'],
        'product_id': prod['product_id'],
        'quantity': quantity,
        'order_date': order_date
    })

df_sales = pd.DataFrame(sales)

# -----------------------------
# 4. Save to CSV
# -----------------------------
df_customers.to_csv('../data/customers.csv', index=False)
df_products.to_csv('../data/products.csv', index=False)
df_sales.to_csv('../data/sales.csv', index=False)

print("✅ CSV files generated and saved to /data folder.")
