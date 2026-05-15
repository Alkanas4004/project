# pages/reports.py

import customtkinter as ctk

from database import cursor
from config import *


class ReportsPage:

    def __init__(self, parent):

        # =========================
        # Main Container
        # =========================
        self.frame = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND_COLOR
        )

        self.frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # =========================
        # Header
        # =========================
        header = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        header.pack(fill="x", pady=(0, 20))

        title = ctk.CTkLabel(
            header,
            text="Reports Dashboard",
            font=TITLE_FONT,
            text_color=TEXT_COLOR
        )

        title.pack(side="left")

        # =========================
        # Statistics Cards
        # =========================
        cards_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        cards_frame.pack(fill="x", pady=(0, 20))

        # Load Statistics
        stats = self.get_statistics()

        # Cards
        self.create_card(
            cards_frame,
            "Total Products",
            stats["total_products"],
            PRIMARY_COLOR,
            0
        )

        self.create_card(
            cards_frame,
            "Stock Quantity",
            stats["total_quantity"],
            SUCCESS_COLOR,
            1
        )

        self.create_card(
            cards_frame,
            "Inventory Value",
            f"{stats['inventory_value']:.2f} EGP",
            WARNING_COLOR,
            2
        )

        self.create_card(
            cards_frame,
            "Low Stock",
            stats["low_stock"],
            DANGER_COLOR,
            3
        )

        # =========================
        # Reports Card
        # =========================
        report_card = ctk.CTkFrame(
            self.frame,
            fg_color=CARD_COLOR,
            corner_radius=FRAME_RADIUS
        )

        report_card.pack(
            fill="both",
            expand=True
        )

        report_title = ctk.CTkLabel(
            report_card,
            text="Inventory Report",
            font=SUBTITLE_FONT,
            text_color=TEXT_COLOR
        )

        report_title.pack(anchor="w", padx=20, pady=(20, 10))

        # =========================
        # Report Textbox
        # =========================
        self.box = ctk.CTkTextbox(
            report_card,
            font=("Consolas", 15),
            corner_radius=12
        )

        self.box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # Generate Report
        self.generate_report()

    # =========================
    # Statistics
    # =========================
    def get_statistics(self):

        cursor.execute("SELECT * FROM products")

        products = cursor.fetchall()

        total_products = len(products)

        total_quantity = sum(
            int(product[5]) for product in products
        )

        inventory_value = sum(
            float(product[3]) * int(product[5])
            for product in products
        )

        low_stock = len([
            product for product in products
            if int(product[5]) <= LOW_STOCK_LIMIT
        ])

        return {
            "total_products": total_products,
            "total_quantity": total_quantity,
            "inventory_value": inventory_value,
            "low_stock": low_stock
        }

    # =========================
    # Create Statistics Card
    # =========================
    def create_card(
        self,
        parent,
        title,
        value,
        color,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            width=250,
            height=140,
            corner_radius=FRAME_RADIUS,
            fg_color=CARD_COLOR
        )

        card.grid(
            row=0,
            column=column,
            padx=10,
            sticky="nsew"
        )

        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            text_color=color
        )

        value_label.pack(pady=(30, 5))

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=TEXT_FONT,
            text_color=TEXT_SECONDARY
        )

        title_label.pack()

    # =========================
    # Generate Report
    # =========================
    def generate_report(self):

        self.box.delete("1.0", "end")

        cursor.execute("""
        SELECT * FROM products
        ORDER BY quantity ASC
        """)

        products = cursor.fetchall()

        if not products:

            self.box.insert(
                "end",
                "No products available..."
            )

            return

        # Header
        self.box.insert(
            "end",
            f"""
{'ID':<5}
{'NAME':<30}
{'BUY':<12}
{'SELL':<12}
{'QTY':<10}

{'='*80}
"""
        )

        # Products
        for product in products:

            stock_alert = ""

            if int(product[5]) <= LOW_STOCK_LIMIT:
                stock_alert = " ⚠ LOW STOCK"

            self.box.insert(
                "end",
                f"""
{product[0]:<5}
{product[1]:<30}
{product[3]:<12}
{product[4]:<12}
{product[5]:<10}
{stock_alert}

{'-'*80}
"""
            )
