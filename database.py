# database.py

import sqlite3
import os
from pathlib import Path


class DatabaseManager:

    def __init__(self):

        # Create Database Folder
        Path("database").mkdir(exist_ok=True)

        # Database Connection
        self.conn = sqlite3.connect(
            "database/supermarket.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        # Enable Foreign Keys
        self.cursor.execute("PRAGMA foreign_keys = ON")

        # Create Tables
        self.create_tables()

        # Create Default Admin
        self.create_default_admin()

    # =========================
    # Create All Tables
    # =========================
    def create_tables(self):

        # Products Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            barcode TEXT UNIQUE NOT NULL,
            buy_price REAL NOT NULL,
            sell_price REAL NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Sales Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL,
            payment_method TEXT DEFAULT 'Cash',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Sale Items Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price REAL,

            FOREIGN KEY (sale_id)
            REFERENCES sales(id)
            ON DELETE CASCADE,

            FOREIGN KEY (product_id)
            REFERENCES products(id)
            ON DELETE CASCADE
        )
        """)

        # Users Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'cashier',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    # =========================
    # Create Default Admin
    # =========================
    def create_default_admin(self):

        self.cursor.execute("""
        INSERT OR IGNORE INTO users(
            id,
            username,
            password,
            role
        )
        VALUES(
            1,
            'admin',
            'admin123',
            'admin'
        )
        """)

        self.conn.commit()

    # =========================
    # Execute Query
    # =========================
    def execute(self, query, params=()):

        self.cursor.execute(query, params)

        self.conn.commit()

    # =========================
    # Fetch One
    # =========================
    def fetchone(self):

        return self.cursor.fetchone()

    # =========================
    # Fetch All
    # =========================
    def fetchall(self):

        return self.cursor.fetchall()

    # =========================
    # Close Connection
    # =========================
    def close(self):

        self.conn.close()


# =========================
# Global Database Object
# =========================
db = DatabaseManager()

conn = db.conn
cursor = db.cursor
