# pages/cashier.py

import customtkinter as ctk

from services.sales_service import SalesService
from services.invoice_service import InvoiceService

from config import *


class CashierPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.total = 0

        self.cart_items = []

        self.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.build_ui()

    # =====================================
    # UI
    # =====================================
    def build_ui(self):

        self.configure(
            fg_color=BACKGROUND_COLOR
        )

        # =====================================
        # Title
        # =====================================
        title = ctk.CTkLabel(
            self,
            text="Cashier System",
            font=TITLE_FONT,
            text_color=TEXT_COLOR
        )

        title.pack(
            anchor="w",
            pady=(10, 20)
        )

        # =====================================
        # Top Frame
        # =====================================
        top_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top_frame.pack(
            fill="x"
        )

        # =====================================
        # Barcode Entry
        # =====================================
        self.barcode_entry = ctk.CTkEntry(
            top_frame,
            placeholder_text="Scan Barcode...",
            width=500,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.barcode_entry.pack(
            side="left",
            padx=(0, 15)
        )

        self.barcode_entry.bind(
            "<Return>",
            lambda event: self.add_product()
        )

        # =====================================
        # Add Button
        # =====================================
        add_btn = ctk.CTkButton(
            top_frame,
            text="Add Product",
            width=170,
            height=BUTTON_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            fg_color=PRIMARY_COLOR,
            hover_color=PRIMARY_HOVER,
            font=BUTTON_FONT,
            command=self.add_product
        )

        add_btn.pack(
            side="left"
        )

        # =====================================
        # Cart Card
        # =====================================
        cart_frame = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=FRAME_RADIUS
        )

        cart_frame.pack(
            fill="both",
            expand=True,
            pady=25
        )

        # =====================================
        # Cart Title
        # =====================================
        cart_title = ctk.CTkLabel(
            cart_frame,
            text="Shopping Cart",
            font=SUBTITLE_FONT,
            text_color=TEXT_COLOR
        )

        cart_title.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        # =====================================
        # Cart Box
        # =====================================
        self.cart_box = ctk.CTkTextbox(
            cart_frame,
            font=("Consolas", 15),
            corner_radius=12
        )

        self.cart_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # =====================================
        # Bottom Frame
        # =====================================
        bottom_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        bottom_frame.pack(
            fill="x"
        )

        # =====================================
        # Total Label
        # =====================================
        self.total_label = ctk.CTkLabel(
            bottom_frame,
            text="Total: 0.00 EGP",
            font=("Segoe UI", 30, "bold"),
            text_color=SUCCESS_COLOR
        )

        self.total_label.pack(
            side="left"
        )

        # =====================================
        # Checkout Button
        # =====================================
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

        checkout_btn.pack(
            side="right"
        )

        # =====================================
        # Clear Cart Button
        # =====================================
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

        clear_btn.pack(
            side="right",
            padx=15
        )

    # =====================================
    # Add Product
    # =====================================
    def add_product(self):

        barcode = self.barcode_entry.get().strip()

        if not barcode:
            return

        product = SalesService.get_product_by_barcode(
            barcode
        )

        # =====================================
        # Product Not Found
        # =====================================
        if not product:

            self.cart_box.insert(
                "end",
                "❌ Product not found\n"
            )

            self.barcode_entry.delete(0, "end")

            return

        # =====================================
        # Out Of Stock
        # =====================================
        if product["quantity"] <= 0:

            self.cart_box.insert(
                "end",
                f"❌ {product['name']} is out of stock\n"
            )

            self.barcode_entry.delete(0, "end")

            return

        # =====================================
        # Add To Cart
        # =====================================
        self.cart_items.append(product)

        self.total += product["sell_price"]

        self.total_label.configure(
            text=f"Total: {self.total:.2f} EGP"
        )

        self.cart_box.insert(
            "end",
            f"""
Product : {product['name']}
Price   : {product['sell_price']} EGP
----------------------------------------
"""
        )

        # =====================================
        # Update Stock
        # =====================================
        SalesService.update_stock(
            product["id"]
        )

        # =====================================
        # Clear Entry
        # =====================================
        self.barcode_entry.delete(0, "end")

    # =====================================
    # Checkout
    # =====================================
    def checkout(self):

        if not self.cart_items:

            self.cart_box.insert(
                "end",
                "❌ Cart is empty\n"
            )

            return

        # =====================================
        # Create Sale
        # =====================================
        sale_id = SalesService.create_sale(
            self.total,
            self.cart_items
        )

        # =====================================
        # Generate Invoice
        # =====================================
        InvoiceService.generate_invoice(
            sale_id=sale_id,
            items=self.cart_items,
            total=self.total
        )

        # =====================================
        # Success Message
        # =====================================
        self.cart_box.insert(
            "end",
            "\n✅ Sale Completed Successfully\n"
        )

        self.cart_box.insert(
            "end",
            f"🧾 Invoice Generated : invoice_{sale_id}.pdf\n\n"
        )

        # =====================================
        # Reset
        # =====================================
        self.total = 0

        self.cart_items.clear()

        self.total_label.configure(
            text="Total: 0.00 EGP"
        )

    # =====================================
    # Clear Cart
    # =====================================
    def clear_cart(self):

        self.cart_box.delete(
            "1.0",
            "end"
        )

        self.total = 0

        self.cart_items.clear()

        self.total_label.configure(
            text="Total: 0.00 EGP"
        )
