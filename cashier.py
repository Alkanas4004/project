# pages/cashier.py

import customtkinter as ctk

from database import conn, cursor
from config import *


class CashierPage:

    def __init__(self, parent):

        self.total = 0
        self.cart_items = []

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
            text="Cashier System",
            font=TITLE_FONT,
            text_color=TEXT_COLOR
        )

        title.pack(anchor="w", pady=(10, 20))

        # =========================
        # Top Section
        # =========================
        top_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        top_frame.pack(fill="x")

        # Barcode Entry
        self.barcode = ctk.CTkEntry(
            top_frame,
            placeholder_text="Scan Barcode...",
            width=500,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.barcode.pack(side="left", padx=(0, 15))

        # Enter Key Support
        self.barcode.bind(
            "<Return>",
            lambda event: self.add_product()
        )

        # Add Product Button
        add_btn = ctk.CTkButton(
            top_frame,
            text="Add Product",
            width=170,
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            fg_color=PRIMARY_COLOR,
            hover_color="#1D4ED8",
            font=BUTTON_FONT,
            command=self.add_product
        )

        add_btn.pack(side="left")

        # =========================
        # Cart Section
        # =========================
        cart_frame = ctk.CTkFrame(
            self.frame,
            fg_color=CARD_COLOR,
            corner_radius=FRAME_RADIUS
        )

        cart_frame.pack(
            fill="both",
            expand=True,
            pady=25
        )

        # Cart Title
        cart_title = ctk.CTkLabel(
            cart_frame,
            text="Shopping Cart",
            font=SUBTITLE_FONT,
            text_color=TEXT_COLOR
        )

        cart_title.pack(anchor="w", padx=20, pady=15)

        # Cart Box
        self.cart = ctk.CTkTextbox(
            cart_frame,
            width=1200,
            height=450,
            font=("Consolas", 16),
            corner_radius=12
        )

        self.cart.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # =========================
        # Bottom Section
        # =========================
        bottom_frame = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )

        bottom_frame.pack(fill="x")

        # Total Label
        self.total_label = ctk.CTkLabel(
            bottom_frame,
            text="Total: 0.00 EGP",
            font=("Segoe UI", 30, "bold"),
            text_color=SUCCESS_COLOR
        )

        self.total_label.pack(side="left")

        # Checkout Button
        checkout_btn = ctk.CTkButton(
            bottom_frame,
            text="Checkout",
            width=200,
            height=55,
            corner_radius=BUTTON_RADIUS,
            fg_color=SUCCESS_COLOR,
            hover_color="#16A34A",
            font=BUTTON_FONT,
            command=self.checkout
        )

        checkout_btn.pack(side="right")

        # Clear Cart Button
        clear_btn = ctk.CTkButton(
            bottom_frame,
            text="Clear Cart",
            width=170,
            height=55,
            corner_radius=BUTTON_RADIUS,
            fg_color=DANGER_COLOR,
            hover_color="#DC2626",
            font=BUTTON_FONT,
            command=self.clear_cart
        )

        clear_btn.pack(side="right", padx=15)

    # =========================
    # Add Product
    # =========================
    def add_product(self):

        barcode = self.barcode.get().strip()

        if not barcode:
            return

        cursor.execute(
            """
            SELECT * FROM products
            WHERE barcode=?
            """,
            (barcode,)
        )

        product = cursor.fetchone()

        # Product Exists
        if product:

            # Check Stock
            if int(product[5]) <= 0:

                self.cart.insert(
                    "end",
                    f"❌ {product[1]} is out of stock\n"
                )

                return

            # Add To Cart
            self.cart.insert(
                "end",
                f"""
Product : {product[1]}
Price   : {product[4]} EGP
------------------------------
"""
            )

            self.total += float(product[4])

            self.total_label.configure(
                text=f"Total: {self.total:.2f} EGP"
            )

            self.cart_items.append(product)

            # Update Stock
            cursor.execute(
                """
                UPDATE products
                SET quantity = quantity - 1
                WHERE id=?
                """,
                (product[0],)
            )

            conn.commit()

        # Product Not Found
        else:

            self.cart.insert(
                "end",
                "❌ Product not found\n"
            )

        # Clear Entry
        self.barcode.delete(0, "end")

    # =========================
    # Checkout
    # =========================
    def checkout(self):

        if not self.cart_items:
            return

        # Save Sale
        cursor.execute(
            """
            INSERT INTO sales(total)
            VALUES(?)
            """,
            (self.total,)
        )

        sale_id = cursor.lastrowid

        # Save Sale Items
        for product in self.cart_items:

            cursor.execute(
                """
                INSERT INTO sale_items(
                    sale_id,
                    product_id,
                    quantity,
                    price
                )
                VALUES(?,?,?,?)
                """,
                (
                    sale_id,
                    product[0],
                    1,
                    product[4]
                )
            )

        conn.commit()

        # Success Message
        self.cart.insert(
            "end",
            "\n✅ Sale Completed Successfully\n\n"
        )

        # Reset
        self.total = 0
        self.cart_items.clear()

        self.total_label.configure(
            text="Total: 0.00 EGP"
        )

    # =========================
    # Clear Cart
    # =========================
    def clear_cart(self):

        self.cart.delete("1.0", "end")

        self.total = 0

        self.cart_items.clear()

        self.total_label.configure(
            text="Total: 0.00 EGP"
        )
