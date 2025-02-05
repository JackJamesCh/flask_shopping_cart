import sqlite3
import json

# Load product data from JSON file
with open('products.json', 'r') as file:
    products = json.load(file)

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Ensure the 'products' table exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image TEXT NOT NULL,
    featured BOOLEAN NOT NULL
)
''')

# Insert data into 'products' table
for product in products:
    cursor.execute('''
    INSERT INTO products (name, price, image, featured)
    VALUES (?, ?, ?, ?)
    ''', (product['name'], product['price'], product['image'], product['featured']))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Product data successfully inserted into the database!")
