# pages/cashier.py

import customtkinter as ctk
from tkinter import ttk, messagebox

from services.sales_service import SalesService
from services.invoice_service import InvoiceService

from config import *


class CashierPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.total = 0
        self.cart_items = []
        self.selected_cart_index = None

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

        # Barcode Entry
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

        # Add Button
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

        # Cart Title
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
        # Table Style
        # =====================================
        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#1E293B",
            foreground="white",
            rowheight=35,
            fieldbackground="#1E293B",
            borderwidth=0,
            font=("Segoe UI", 12)
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 12, "bold")
        )

        # =====================================
        # Cart Table
        # =====================================
        columns = (
            "ID",
            "Product",
            "Price",
            "Quantity",
            "Total"
        )

        self.cart_table = ttk.Treeview(
            cart_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:

            self.cart_table.heading(
                col,
                text=col
            )

            self.cart_table.column(
                col,
                width=130,
                anchor="center"
            )

        self.cart_table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.cart_table.bind(
            "<Double-1>",
            self.select_cart_item
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

        # Total Label
        self.total_label = ctk.CTkLabel(
            bottom_frame,
            text="Total: 0.00 EGP",
            font=("Segoe UI", 30, "bold"),
            text_color=SUCCESS_COLOR
        )

        self.total_label.pack(
            side="left"
        )

        # Checkout Button
        checkout_btn = ctk.CTkButton(
            bottom_frame,
            text="Checkout",
            width=180,
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

        clear_btn.pack(
            side="right",
            padx=15
        )

        # Remove Item Button
        remove_btn = ctk.CTkButton(
            bottom_frame,
            text="Remove Item",
            width=170,
            height=55,
            corner_radius=BUTTON_RADIUS,
            fg_color=WARNING_COLOR,
            hover_color="#D97706",
            font=BUTTON_FONT,
            command=self.remove_cart_item
        )

        remove_btn.pack(
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

        # Product Not Found
        if not product:

            messagebox.showerror(
                "Error",
                "Product not found"
            )

            self.barcode_entry.delete(0, "end")

            return

        # Out Of Stock
        if product["quantity"] <= 0:

            messagebox.showwarning(
                "Out Of Stock",
                f"{product['name']} is out of stock"
            )

            self.barcode_entry.delete(0, "end")

            return

        # =====================================
        # Add / Update Cart
        # =====================================
        existing = None

        for item in self.cart_items:

            if item["id"] == product["id"]:

                existing = item

                break

        if existing:

            existing["cart_qty"] += 1

        else:

            product["cart_qty"] = 1

            self.cart_items.append(product)

        self.total += product["sell_price"]

        self.total_label.configure(
            text=f"Total: {self.total:.2f} EGP"
        )

        self.refresh_cart()

        # Update Stock
        SalesService.update_stock(
            product["id"]
        )

        # Clear Entry
        self.barcode_entry.delete(0, "end")

    # =====================================
    # Refresh Cart
    # =====================================
    def refresh_cart(self):

        for row in self.cart_table.get_children():

            self.cart_table.delete(row)

        for item in self.cart_items:

            qty = item.get("cart_qty", 1)

            self.cart_table.insert(
                "",
                "end",
                values=(
                    item["id"],
                    item["name"],
                    item["sell_price"],
                    qty,
                    item["sell_price"] * qty
                )
            )

    # =====================================
    # Select Cart Item
    # =====================================
    def select_cart_item(self, event):

        selected = self.cart_table.focus()

        values = self.cart_table.item(
            selected,
            "values"
        )

        if not values:
            return

        self.selected_cart_index = values[0]

    # =====================================
    # Remove Cart Item
    # =====================================
    def remove_cart_item(self):

        if not self.selected_cart_index:
            return

        for item in self.cart_items:

            if str(item["id"]) == str(self.selected_cart_index):

                qty = item.get("cart_qty", 1)

                self.total -= item["sell_price"] * qty

                self.cart_items.remove(item)

                break

        self.total_label.configure(
            text=f"Total: {self.total:.2f} EGP"
        )

        self.refresh_cart()

        self.selected_cart_index = None

    # =====================================
    # Checkout
    # =====================================
    def checkout(self):

        if not self.cart_items:

            messagebox.showwarning(
                "Empty Cart",
                "Cart is empty"
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Checkout",
            f"Total Bill: {self.total:.2f} EGP\nProceed?"
        )

        if not confirm:
            return

        # Create Sale
        sale_id = SalesService.create_sale(
            self.total,
            self.cart_items
        )

        # Generate Invoice
        InvoiceService.generate_invoice(
            sale_id=sale_id,
            items=self.cart_items,
            total=self.total
        )

        # Success
        messagebox.showinfo(
            "Success",
            f"Sale Completed Successfully\nInvoice: invoice_{sale_id}.pdf"
        )

        # Reset
        self.clear_cart()

    # =====================================
    # Clear Cart
    # =====================================
    def clear_cart(self):

        for row in self.cart_table.get_children():

            self.cart_table.delete(row)

        self.total = 0

        self.cart_items.clear()

        self.total_label.configure(
            text="Total: 0.00 EGP"
        )
