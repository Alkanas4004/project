# pages/reports.py

import customtkinter as ctk
from database import cursor


class ReportsPage:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        title = ctk.CTkLabel(
            self.frame,
            text="Reports Dashboard",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=20)

        self.box = ctk.CTkTextbox(self.frame, width=1000, height=500)
        self.box.pack(pady=20)

        self.generate_report()

    def generate_report(self):
        self.box.delete("1.0", "end")

        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        total_products = len(products)
        total_quantity = sum(int(product[5]) for product in products)
        inventory_value = sum(
            float(product[3]) * int(product[5]) for product in products
        )

        report = (
            f"Total Products: {total_products}\n"
            f"Total Quantity in Stock: {total_quantity}\n"
            f"Inventory Cost Value: {inventory_value} EGP\n"
            f"{'='*50}\n"
        )

        for product in products:
            report += (
                f"Name: {product[1]} | "
                f"Barcode: {product[2]} | "
                f"Buy: {product[3]} | "
                f"Sell: {product[4]} | "
                f"Qty: {product[5]}\n"
            )

        self.box.insert("end", report)
