# pages/products.py

import customtkinter as ctk

from database import conn, cursor
from config import *


class ProductsPage:

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
        # Page Title
        # =========================
        title = ctk.CTkLabel(
            self.frame,
            text="Products Management",
            font=TITLE_FONT,
            text_color=TEXT_COLOR
        )

        title.pack(anchor="w", pady=(10, 25))

        # =========================
        # Form Card
        # =========================
        form_frame = ctk.CTkFrame(
            self.frame,
            fg_color=CARD_COLOR,
            corner_radius=FRAME_RADIUS
        )

        form_frame.pack(fill="x", pady=(0, 20))

        # =========================
        # Form Inputs
        # =========================
        inputs_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )

        inputs_frame.pack(padx=20, pady=20)

        self.name = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Product Name",
            width=260,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.name.grid(row=0, column=0, padx=10, pady=10)

        self.barcode = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Barcode",
            width=260,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.barcode.grid(row=0, column=1, padx=10, pady=10)

        self.buy = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Buy Price",
            width=260,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.buy.grid(row=1, column=0, padx=10, pady=10)

        self.sell = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Sell Price",
            width=260,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.sell.grid(row=1, column=1, padx=10, pady=10)

        self.qty = ctk.CTkEntry(
            inputs_frame,
            placeholder_text="Quantity",
            width=260,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.qty.grid(row=2, column=0, padx=10, pady=10)

        # =========================
        # Save Button
        # =========================
        save_btn = ctk.CTkButton(
            inputs_frame,
            text="Save Product",
            width=260,
            height=50,
            corner_radius=BUTTON_RADIUS,
            fg_color=PRIMARY_COLOR,
            hover_color="#1D4ED8",
            font=BUTTON_FONT,
            command=self.save_product
        )

        save_btn.grid(row=2, column=1, padx=10, pady=10)

        # =========================
        # Status Label
        # =========================
        self.status = ctk.CTkLabel(
            form_frame,
            text="",
            font=SMALL_FONT,
            text_color=SUCCESS_COLOR
        )

        self.status.pack(pady=(0, 15))

        # =========================
        # Products List Card
        # =========================
        products_frame = ctk.CTkFrame(
            self.frame,
            fg_color=CARD_COLOR,
            corner_radius=FRAME_RADIUS
        )

        products_frame.pack(
            fill="both",
            expand=True
        )

        # Products Title
        products_title = ctk.CTkLabel(
            products_frame,
            text="Products List",
            font=SUBTITLE_FONT,
            text_color=TEXT_COLOR
        )

        products_title.pack(anchor="w", padx=20, pady=15)

        # Products Textbox
        self.box = ctk.CTkTextbox(
            products_frame,
            font=("Consolas", 15),
            corner_radius=12
        )

        self.box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # Load Products
        self.load_products()

    # =========================
    # Save Product
    # =========================
    def save_product(self):

        name = self.name.get().strip()
        barcode = self.barcode.get().strip()
        buy = self.buy.get().strip()
        sell = self.sell.get().strip()
        qty = self.qty.get().strip()

        # Validation
        if not all([name, barcode, buy, sell, qty]):

            self.status.configure(
                text="Please fill all fields",
                text_color=DANGER_COLOR
            )

            return

        try:

            cursor.execute(
                """
                INSERT INTO products(
                    name,
                    barcode,
                    buy_price,
                    sell_price,
                    quantity
                )
                VALUES(?,?,?,?,?)
                """,
                (
                    name,
                    barcode,
                    float(buy),
                    float(sell),
                    int(qty)
                )
            )

            conn.commit()

            self.status.configure(
                text="✅ Product added successfully",
                text_color=SUCCESS_COLOR
            )

            self.clear_fields()

            self.load_products()

        except Exception as e:

            self.status.configure(
                text=f"❌ {e}",
                text_color=DANGER_COLOR
            )

    # =========================
    # Load Products
    # =========================
    def load_products(self):

        self.box.delete("1.0", "end")

        cursor.execute("""
        SELECT * FROM products
        ORDER BY id DESC
        """)

        products = cursor.fetchall()

        if not products:

            self.box.insert(
                "end",
                "No products found..."
            )

            return

        self.box.insert(
            "end",
            f"{'ID':<5} {'NAME':<25} {'PRICE':<15} {'QTY':<10}\n"
        )

        self.box.insert(
            "end",
            "=" * 70 + "\n"
        )

        for product in products:

            self.box.insert(
                "end",
                f"""
{product[0]:<5}
{product[1]:<25}
{product[4]:<15} EGP
{product[5]:<10}
--------------------------------------------
"""
            )

    # =========================
    # Clear Fields
    # =========================
    def clear_fields(self):

        self.name.delete(0, "end")
        self.barcode.delete(0, "end")
        self.buy.delete(0, "end")
        self.sell.delete(0, "end")
        self.qty.delete(0, "end")
