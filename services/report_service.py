from database.connection import DatabaseConnection

from config import LOW_STOCK_LIMIT


class ReportService:

    # =====================================
    # Dashboard Statistics
    # =====================================
    @staticmethod
    def get_statistics():

        db = DatabaseConnection()

        products = db.fetchall(
            """
            SELECT *
            FROM products
            """
        )

        db.close()

        total_products = len(products)

        total_quantity = sum(
            product["quantity"]
            for product in products
        )

        inventory_value = sum(
            product["buy_price"] * product["quantity"]
            for product in products
        )

        low_stock = len([
            product for product in products
            if product["quantity"] <= LOW_STOCK_LIMIT
        ])

        return {
            "total_products": total_products,
            "total_quantity": total_quantity,
            "inventory_value": inventory_value,
            "low_stock": low_stock
        }

    # =====================================
    # Inventory Report
    # =====================================
    @staticmethod
    def get_inventory_report():

        db = DatabaseConnection()

        products = db.fetchall(
            """
            SELECT *
            FROM products
            ORDER BY quantity ASC
            """
        )

        db.close()

        return products
