import customtkinter as ctk

from services.report_service import ReportService

from config import *


class ReportsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.build_ui()

        self.load_statistics()

        self.generate_report()

    # =====================================
    # UI
    # =====================================
    def build_ui(self):

        self.configure(
            fg_color=BACKGROUND_COLOR
        )

        # =====================================
        # Header
        # =====================================
        self.header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.header.pack(
            fill="x",
            pady=(0, 20)
        )

        self.title = ctk.CTkLabel(
            self.header,
            text="Reports Dashboard",
            font=TITLE_FONT,
            text_color=TEXT_COLOR
        )

        self.title.pack(
            side="left"
        )

        # =====================================
        # Statistics Cards Container
        # =====================================
        self.cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.cards_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        # Make Grid Responsive
        for i in range(4):

            self.cards_frame.grid_columnconfigure(
                i,
                weight=1
            )

        # =====================================
        # Report Card
        # =====================================
        self.report_card = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=FRAME_RADIUS
        )

        self.report_card.pack(
            fill="both",
            expand=True
        )

        # =====================================
        # Report Title
        # =====================================
        self.report_title = ctk.CTkLabel(
            self.report_card,
            text="Inventory Report",
            font=SUBTITLE_FONT,
            text_color=TEXT_COLOR
        )

        self.report_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # =====================================
        # Report Textbox
        # =====================================
        self.report_box = ctk.CTkTextbox(
            self.report_card,
            font=("Consolas", 14),
            corner_radius=12
        )

        self.report_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

    # =====================================
    # Load Statistics
    # =====================================
    def load_statistics(self):

        stats = ReportService.get_statistics()

        cards = [
            (
                "Total Products",
                stats["total_products"],
                PRIMARY_COLOR
            ),
            (
                "Stock Quantity",
                stats["total_quantity"],
                SUCCESS_COLOR
            ),
            (
                "Inventory Value",
                f"{stats['inventory_value']:.2f} EGP",
                WARNING_COLOR
            ),
            (
                "Low Stock",
                stats["low_stock"],
                DANGER_COLOR
            )
        ]

        for index, card in enumerate(cards):

            self.create_card(
                title=card[0],
                value=card[1],
                color=card[2],
                column=index
            )

    # =====================================
    # Statistics Card
    # =====================================
    def create_card(
        self,
        title,
        value,
        color,
        column
    ):

        card = ctk.CTkFrame(
            self.cards_frame,
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

        # =====================================
        # Value
        # =====================================
        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            text_color=color
        )

        value_label.pack(
            pady=(30, 5)
        )

        # =====================================
        # Title
        # =====================================
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=TEXT_FONT,
            text_color=TEXT_SECONDARY
        )

        title_label.pack()

    # =====================================
    # Generate Report
    # =====================================
    def generate_report(self):

        self.report_box.delete(
            "1.0",
            "end"
        )

        products = ReportService.get_inventory_report()

        if not products:

            self.report_box.insert(
                "end",
                "No products available..."
            )

            return

        # =====================================
        # Table Header
        # =====================================
        self.report_box.insert(
            "end",
            f"{'ID':<5}"
            f"{'NAME':<30}"
            f"{'BUY':<12}"
            f"{'SELL':<12}"
            f"{'QTY':<10}"
            f"{'STATUS':<15}\n"
        )

        self.report_box.insert(
            "end",
            "=" * 90 + "\n"
        )

        # =====================================
        # Products
        # =====================================
        for product in products:

            status = "GOOD"

            if product["quantity"] <= LOW_STOCK_LIMIT:

                status = "LOW STOCK"

            self.report_box.insert(
                "end",
                f"{product['id']:<5}"
                f"{product['name']:<30}"
                f"{product['buy_price']:<12}"
                f"{product['sell_price']:<12}"
                f"{product['quantity']:<10}"
                f"{status:<15}\n"
            )
