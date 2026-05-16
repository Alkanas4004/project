import sqlite3
from pathlib import Path
import bcrypt
import shutil
from datetime import datetime


class DatabaseManager:

    def __init__(self):

        # =====================================
        # Create Database Folder
        # =====================================
        Path("database").mkdir(
            exist_ok=True
        )

        # =====================================
        # Database Connection
        # =====================================
        self.db_path = "database/supermarket.db"

        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self.conn.row_factory = sqlite3.Row

        self.cursor = self.conn.cursor()

        # Enable Foreign Keys
        self.cursor.execute(
            "PRAGMA foreign_keys = ON"
        )

        # =====================================
        # Setup Database
        # =====================================
        self.create_tables()

        self.create_default_admin()

    # =====================================
    # Create Tables
    # =====================================
    def create_tables(self):

        # Products
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            barcode TEXT UNIQUE NOT NULL,
            category TEXT,
            buy_price REAL NOT NULL,
            sell_price REAL NOT NULL,
            quantity INTEGER DEFAULT 0,
            supplier_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Sales
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            total REAL NOT NULL,
            discount REAL DEFAULT 0,
            tax REAL DEFAULT 0,
            payment_method TEXT DEFAULT 'Cash',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Sale Items
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

        # Users
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'cashier',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Customers
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            points INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Suppliers
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            company TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Purchases
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER,
            total REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (supplier_id)
            REFERENCES suppliers(id)
            ON DELETE SET NULL
        )
        """)

        # Returns
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS returns(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            total REAL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (sale_id)
            REFERENCES sales(id)
            ON DELETE CASCADE
        )
        """)

        # Activity Logs
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            action TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()

    # =====================================
    # Create Default Admin
    # =====================================
    def create_default_admin(self):

        hashed_password = bcrypt.hashpw(
            "admin123".encode(),
            bcrypt.gensalt()
        ).decode()

        self.cursor.execute("""
        INSERT OR IGNORE INTO users(
            id,
            username,
            password,
            role
        )
        VALUES(
            1,
            ?,
            ?,
            ?
        )
        """, (
            "admin",
            hashed_password,
            "admin"
        ))

        self.conn.commit()

    # =====================================
    # Execute Query
    # =====================================
    def execute(
        self,
        query,
        params=()
    ):

        self.cursor.execute(
            query,
            params
        )

        self.conn.commit()

    # =====================================
    # Fetch One
    # =====================================
    def fetchone(self):

        result = self.cursor.fetchone()

        return dict(result) if result else None

    # =====================================
    # Fetch All
    # =====================================
    def fetchall(self):

        results = self.cursor.fetchall()

        return [
            dict(row)
            for row in results
        ]

    # =====================================
    # Backup Database
    # =====================================
    def backup_database(self):

        backup_folder = Path(
            "database/backups"
        )

        backup_folder.mkdir(
            exist_ok=True
        )

        backup_file = backup_folder / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

        self.conn.commit()

        shutil.copy(
            self.db_path,
            backup_file
        )

        return str(backup_file)

    # =====================================
    # Log Activity
    # =====================================
    def log_activity(
        self,
        user,
        action
    ):

        self.execute("""
        INSERT INTO activity_logs(
            user,
            action
        )
        VALUES(
            ?,
            ?
        )
        """, (
            user,
            action
        ))

    # =====================================
    # Close Connection
    # =====================================
    def close(self):

        self.conn.close()


# =====================================
# Global Database Object
# =====================================
db = DatabaseManager()

conn = db.conn

cursor = db.cursor
