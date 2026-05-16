# =====================================
# UPDATED PRODUCTS PAGE (FULL VERSION)
# Add / Search / Refresh / Select / Update / Delete
# =====================================

import customtkinter as ctk

from tkinter import ttk
from tkinter import messagebox

from services.product_service import ProductService

from config import *


class ProductsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.selected_product_id = None

        self.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.build_ui()

        self.load_products()

    # =====================================
    # UI
    # =====================================
    def build_ui(self):

        self.configure(
            fg_color=BACKGROUND_COLOR
        )

        # =====================================
        # Page Title
        # =====================================
        self.title = ctk.CTkLabel(
            self,
            text="Products Management",
            font=TITLE_FONT,
            text_color=TEXT_COLOR
        )

        self.title.pack(
            anchor="w",
            pady=(10, 25)
        )

        # =====================================
        # Form Card
        # =====================================
        self.form_card = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=FRAME_RADIUS
        )

        self.form_card.pack(
            fill="x",
            pady=(0, 20)
        )

        # =====================================
        # Inputs Frame
        # =====================================
        self.inputs_frame = ctk.CTkFrame(
            self.form_card,
            fg_color="transparent"
        )

        self.inputs_frame.pack(
            padx=20,
            pady=20
        )

        # =====================================
        # Entries
        # =====================================
        self.name_entry = self.create_entry(
            "Product Name",
            0,
            0
        )

        self.barcode_entry = self.create_entry(
            "Barcode",
            0,
            1
        )

        self.buy_entry = self.create_entry(
            "Buy Price",
            1,
            0
        )

        self.sell_entry = self.create_entry(
            "Sell Price",
            1,
            1
        )

        self.qty_entry = self.create_entry(
            "Quantity",
            2,
            0
        )

        # =====================================
        # Save Button
        # =====================================
        self.save_button = ctk.CTkButton(
            self.inputs_frame,
            text="Save Product",
            width=180,
            height=50,
            corner_radius=BUTTON_RADIUS,
            fg_color=PRIMARY_COLOR,
            hover_color=PRIMARY_HOVER,
            font=BUTTON_FONT,
            command=self.save_product
        )

        self.save_button.grid(
            row=2,
            column=1,
            padx=10,
            pady=10,
            sticky="w"
        )

        # =====================================
        # Update Button
        # =====================================
        self.update_button = ctk.CTkButton(
            self.inputs_frame,
            text="Update Product",
            width=180,
            height=50,
            corner_radius=BUTTON_RADIUS,
            fg_color=WARNING_COLOR,
            hover_color="#D97706",
            font=BUTTON_FONT,
            command=self.update_product
        )

        self.update_button.grid(
            row=3,
            column=0,
            padx=10,
            pady=10
        )

        # =====================================
        # Delete Button
        # =====================================
        self.delete_button = ctk.CTkButton(
            self.inputs_frame,
            text="Delete Product",
            width=180,
            height=50,
            corner_radius=BUTTON_RADIUS,
            fg_color=DANGER_COLOR,
            hover_color="#DC2626",
            font=BUTTON_FONT,
            command=self.delete_product
        )

        self.delete_button.grid(
            row=3,
            column=1,
            padx=10,
            pady=10,
            sticky="w"
        )

        # =====================================
        # Status Label
        # =====================================
        self.status_label = ctk.CTkLabel(
            self.form_card,
            text="",
            font=SMALL_FONT
        )

        self.status_label.pack(
            pady=(0, 15)
        )

        # =====================================
        # Products Card
        # =====================================
        self.products_card = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=FRAME_RADIUS
        )

        self.products_card.pack(
            fill="both",
            expand=True
        )

        # =====================================
        # Products Title
        # =====================================
        self.products_title = ctk.CTkLabel(
            self.products_card,
            text="Products List",
            font=SUBTITLE_FONT,
            text_color=TEXT_COLOR
        )

        self.products_title.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        # =====================================
        # Search Frame
        # =====================================
        self.search_frame = ctk.CTkFrame(
            self.products_card,
            fg_color="transparent"
        )

        self.search_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        # =====================================
        # Search Entry
        # =====================================
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search product...",
            width=300,
            height=40
        )

        self.search_entry.pack(
            side="left",
            padx=(0, 10)
        )

        # =====================================
        # Search Button
        # =====================================
        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=120,
            command=self.search_products
        )

        self.search_button.pack(
            side="left"
        )

        # =====================================
        # Refresh Button
        # =====================================
        self.refresh_button = ctk.CTkButton(
            self.search_frame,
            text="Refresh",
            width=120,
            fg_color=SUCCESS_COLOR,
            hover_color="#16A34A",
            command=self.load_products
        )

        self.refresh_button.pack(
            side="left",
            padx=10
        )

        # =====================================
        # Table Frame
        # =====================================
        self.table_frame = ctk.CTkFrame(
            self.products_card
        )

        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
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
        # Table Columns
        # =====================================
        columns = (
            "ID",
            "Name",
            "Barcode",
            "Buy Price",
            "Sell Price",
            "Quantity"
        )

        self.products_table = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:

            self.products_table.heading(
                col,
                text=col
            )

            self.products_table.column(
                col,
                anchor="center",
                width=140
            )

        self.products_table.pack(
            fill="both",
            expand=True
        )

        # =====================================
        # Select Product
        # =====================================
        self.products_table.bind(
            "<Double-1>",
            self.select_product
        )

    # =====================================
    # Entry Creator
    # =====================================
    def create_entry(self, placeholder, row, column):

        entry = ctk.CTkEntry(
            self.inputs_frame,
            placeholder_text=placeholder,
            width=260,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        entry.grid(
            row=row,
            column=column,
            padx=10,
            pady=10
        )

        return entry

    # =====================================
    # Save Product
    # =====================================
    def save_product(self):

        name = self.name_entry.get().strip()
        barcode = self.barcode_entry.get().strip()
        buy_price = self.buy_entry.get().strip()
        sell_price = self.sell_entry.get().strip()
        quantity = self.qty_entry.get().strip()

        if not all([name, barcode, buy_price, sell_price, quantity]):

            self.show_message(
                "Please fill all fields",
                DANGER_COLOR
            )

            return

        try:

            buy_price = float(buy_price)
            sell_price = float(sell_price)
            quantity = int(quantity)

        except ValueError:

            self.show_message(
                "Invalid numeric values",
                DANGER_COLOR
            )

            return

        success, message = ProductService.add_product(
            name,
            barcode,
            buy_price,
            sell_price,
            quantity
        )

        if success:

            self.show_message(
                message,
                SUCCESS_COLOR
            )

            self.clear_fields()

            self.load_products()

        else:

            self.show_message(
                message,
                DANGER_COLOR
            )

    # =====================================
    # Update Product
    # =====================================
    def update_product(self):

        if not self.selected_product_id:

            self.show_message(
                "Select product first",
                DANGER_COLOR
            )

            return

        success, message = ProductService.update_product(
            self.selected_product_id,
            self.name_entry.get().strip(),
            self.barcode_entry.get().strip(),
            float(self.buy_entry.get()),
            float(self.sell_entry.get()),
            int(self.qty_entry.get())
        )

        if success:

            self.show_message(
                message,
                SUCCESS_COLOR
            )

            self.load_products()

            self.clear_fields()

        else:

            self.show_message(
                message,
                DANGER_COLOR
            )

    # =====================================
    # Load Products
    # =====================================
    def load_products(self):

        for row in self.products_table.get_children():
            self.products_table.delete(row)

        products = ProductService.get_products()

        for product in products:

            self.products_table.insert(
                "",
                "end",
                values=(
                    product["id"],
                    product["name"],
                    product["barcode"],
                    product["buy_price"],
                    product["sell_price"],
                    product["quantity"]
                )
            )

    # =====================================
    # Search Products
    # =====================================
    def search_products(self):

        keyword = self.search_entry.get().strip().lower()

        for row in self.products_table.get_children():
            self.products_table.delete(row)

        products = ProductService.get_products()

        for product in products:

            if (
                keyword in product["name"].lower()
                or
                keyword in product["barcode"].lower()
            ):

                self.products_table.insert(
                    "",
                    "end",
                    values=(
                        product["id"],
                        product["name"],
                        product["barcode"],
                        product["buy_price"],
                        product["sell_price"],
                        product["quantity"]
                    )
                )

    # =====================================
    # Select Product
    # =====================================
    def select_product(self, event):

        selected = self.products_table.focus()

        values = self.products_table.item(
            selected,
            "values"
        )

        if not values:
            return

        self.selected_product_id = values[0]

        self.clear_fields()

        self.name_entry.insert(0, values[1])
        self.barcode_entry.insert(0, values[2])
        self.buy_entry.insert(0, values[3])
        self.sell_entry.insert(0, values[4])
        self.qty_entry.insert(0, values[5])

    # =====================================
    # Delete Product
    # =====================================
    def delete_product(self):

        if not self.selected_product_id:

            self.show_message(
                "Select product first",
                DANGER_COLOR
            )

            return

        confirm = messagebox.askyesno(
            "Delete Product",
            "Are you sure?"
        )

        if not confirm:
            return

        success, message = ProductService.delete_product(
            self.selected_product_id
        )

        if success:

            self.show_message(
                message,
                SUCCESS_COLOR
            )

            self.clear_fields()

            self.load_products()

            self.selected_product_id = None

        else:

            self.show_message(
                message,
                DANGER_COLOR
            )

    # =====================================
    # Clear Fields
    # =====================================
    def clear_fields(self):

        self.name_entry.delete(0, "end")
        self.barcode_entry.delete(0, "end")
        self.buy_entry.delete(0, "end")
        self.sell_entry.delete(0, "end")
        self.qty_entry.delete(0, "end")

    # =====================================
    # Status Message
    # =====================================
    def show_message(self, message, color):

        self.status_label.configure(
            text=message,
            text_color=color
        )
