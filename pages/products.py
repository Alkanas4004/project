import customtkinter as ctk

from services.product_service import ProductService

from config import *


class ProductsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

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
        # Inputs Container
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
        # Product Name
        # =====================================
        self.name_entry = self.create_entry(
            "Product Name",
            0,
            0
        )

        # =====================================
        # Barcode
        # =====================================
        self.barcode_entry = self.create_entry(
            "Barcode",
            0,
            1
        )

        # =====================================
        # Buy Price
        # =====================================
        self.buy_entry = self.create_entry(
            "Buy Price",
            1,
            0
        )

        # =====================================
        # Sell Price
        # =====================================
        self.sell_entry = self.create_entry(
            "Sell Price",
            1,
            1
        )

        # =====================================
        # Quantity
        # =====================================
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
            width=260,
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
            pady=10
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
        # Products List Card
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
        # Products Textbox
        # =====================================
        self.products_box = ctk.CTkTextbox(
            self.products_card,
            font=("Consolas", 15),
            corner_radius=12
        )

        self.products_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    # =====================================
    # Create Entry Helper
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

        # =====================================
        # Validation
        # =====================================
        if not all([
            name,
            barcode,
            buy_price,
            sell_price,
            quantity
        ]):

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

        # =====================================
        # Disable Button
        # =====================================
        self.save_button.configure(
            state="disabled",
            text="Saving..."
        )

        # =====================================
        # Save Product
        # =====================================
        success, message = ProductService.add_product(
            name=name,
            barcode=barcode,
            buy_price=buy_price,
            sell_price=sell_price,
            quantity=quantity
        )

        # =====================================
        # Result
        # =====================================
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
        # Enable Button Again
        # =====================================
        self.save_button.configure(
            state="normal",
            text="Save Product"
        )

    # =====================================
    # Load Products
    # =====================================
    def load_products(self):

        self.products_box.delete(
            "1.0",
            "end"
        )

        products = ProductService.get_products()

        if not products:

            self.products_box.insert(
                "end",
                "No products found..."
            )

            return

        # =====================================
        # Table Header
        # =====================================
        self.products_box.insert(
            "end",
            f"{'ID':<5}"
            f"{'NAME':<25}"
            f"{'PRICE':<15}"
            f"{'QTY':<10}\n"
        )

        self.products_box.insert(
            "end",
            "=" * 70 + "\n"
        )

        # =====================================
        # Products
        # =====================================
        for product in products:

            self.products_box.insert(
                "end",
                f"{product['id']:<5}"
                f"{product['name']:<25}"
                f"{product['sell_price']:<15} EGP"
                f"{product['quantity']:<10}\n"
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
    # Show Message
    # =====================================
    def show_message(self, message, color):

        self.status_label.configure(
            text=message,
            text_color=color
        )
