# database.py

import sqlite3
import os

# Ensure database folder exists
os.makedirs("database", exist_ok=True)

# Database connection
conn = sqlite3.connect("database/supermarket.db")
cursor = conn.cursor()

# Products Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    barcode TEXT UNIQUE NOT NULL,
    buy_price REAL NOT NULL,
    sell_price REAL NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0
)
""")

# Sales Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Sale Items Table (for invoice details)
cursor.execute("""
CREATE TABLE IF NOT EXISTS sale_items(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY (sale_id) REFERENCES sales(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

# Users Table (for future login system)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'cashier'
)
""")

# Default admin account
cursor.execute("""
INSERT OR IGNORE INTO users(username, password, role)
VALUES('admin', 'admin123', 'admin')
""")

# Commit changes
conn.commit()
