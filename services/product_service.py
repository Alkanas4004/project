from database.connection import DatabaseConnection


class ProductService:

    @staticmethod
    def add_product(
        name,
        barcode,
        buy_price,
        sell_price,
        quantity
    ):

        db = DatabaseConnection()

        # =====================================
        # Check Barcode Exists
        # =====================================
        existing = db.fetchone(
            """
            SELECT id
            FROM products
            WHERE barcode = ?
            """,
            (barcode,)
        )

        if existing:

            db.close()

            return False, "Barcode already exists"

        # =====================================
        # Insert Product
        # =====================================
        try:

            db.execute(
                """
                INSERT INTO products(
                    name,
                    barcode,
                    buy_price,
                    sell_price,
                    quantity
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    name,
                    barcode,
                    buy_price,
                    sell_price,
                    quantity
                )
            )

            db.close()

            return True, "✅ Product added successfully"

        except Exception as e:

            db.close()

            return False, str(e)

    # =====================================
    # Get Products
    # =====================================
    @staticmethod
    def get_products():

        db = DatabaseConnection()

        db.cursor.row_factory = dict_factory

        products = db.fetchall(
            """
            SELECT *
            FROM products
            ORDER BY id DESC
            """
        )

        db.close()

        return products


# =====================================
# SQLite Dict Factory
# =====================================
def dict_factory(cursor, row):

    fields = [column[0] for column in cursor.description]

    return {
        key: value
        for key, value in zip(fields, row)
    }
