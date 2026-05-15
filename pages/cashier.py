import customtkinter as ctk
from database import conn, cursor

class CashierPage:

    def __init__(self, parent):

        self.total = 0

        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True)

        self.barcode = ctk.CTkEntry(
            frame,
            placeholder_text="Scan Barcode",
            width=500
        )

        self.barcode.pack(pady=10)

        btn = ctk.CTkButton(
            frame,
            text="Add Product",
            command=self.add_product
        )

        btn.pack(pady=10)

        self.cart = ctk.CTkTextbox(frame, width=1000, height=400)
        self.cart.pack(pady=20)

        self.total_label = ctk.CTkLabel(
            frame,
            text="Total: 0 EGP",
            font=("Arial", 30)
        )

        self.total_label.pack(pady=20)

    def add_product(self):

        cursor.execute(
            "SELECT * FROM products WHERE barcode=?",
            (self.barcode.get(),)
        )

        product = cursor.fetchone()

        if product:

            self.cart.insert(
                "end",
                f"{product[1]} - {product[4]} EGP\n"
            )

            self.total += float(product[4])

            self.total_label.configure(
                text=f"Total: {self.total} EGP"
            )

            cursor.execute(
                "UPDATE products SET quantity=quantity-1 WHERE id=?",
                (product[0],)
            )

            conn.commit()
