import sqlite3
from model.Product import Product

class ProductDao:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self._create_table()

    def _connect(self):
        """Establish a database connection."""
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        """Ensure the 'products' table exists."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                name TEXT NOT NULL PRIMARY KEY,
                price REAL NOT NULL,
                image TEXT NOT NULL,
                featured BOOLEAN NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def insert_product(self, product):
        """Insert a new product into the database."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, price, image, featured)
            VALUES (?, ?, ?, ?)
        ''', (product.name, product.price, product.image, product.featured))
        conn.commit()
        conn.close()

    def get_all_products(self):
        """Retrieve all products from the database."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()
        return [Product(name=row[0], price=row[1], image=row[2], featured=bool(row[3])).to_dict() for row in rows]

    def get_all_featured_products(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE featured = 1")
        rows = cursor.fetchall()
        conn.close()
        return [Product(name=row[0], price=row[1], image=row[2], featured=bool(row[3])).to_dict() for row in rows]



    def get_product_by_name(self, product_name):
        """Retrieve a single product by ID."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name = ?", (product_name,))
        row = cursor.fetchone()
        conn.close()
        return Product(name=row[0], price=row[1], image=row[2], featured=bool(row[3])) if row else None

    def update_product(self, product):
        """Update an existing product."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE products SET name = ?, price = ?, featured = ?
            WHERE name = ?
        ''', (product.name, product.price, product.featured, product.name))
        conn.commit()
        conn.close()

    def delete_product(self, product_name):
        """Delete a product from the database."""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE name = ?", (product_name,))
        conn.commit()
        conn.close()
