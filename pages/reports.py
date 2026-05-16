# =====================================
# إضافات جديدة داخل pages/reports.py
# =====================================
# 1- زر تحديث التقرير
# 2- زر تصدير التقرير TXT
# 3- قسم ملخص المبيعات
# 4- تحسين شكل التقرير
# =====================================

import customtkinter as ctk
from tkinter import filedialog

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
        # Refresh Button
        # =====================================
        self.refresh_button = ctk.CTkButton(
            self.header,
            text="Refresh",
            width=120,
            fg_color=PRIMARY_COLOR,
            hover_color=PRIMARY_HOVER,
            command=self.refresh_data
        )

        self.refresh_button.pack(
            side="right",
            padx=10
        )

        # =====================================
        # Export Button
        # =====================================
        self.export_button = ctk.CTkButton(
            self.header,
            text="Export Report",
            width=150,
            fg_color=SUCCESS_COLOR,
            hover_color="#16A34A",
            command=self.export_report
        )

        self.export_button.pack(
            side="right"
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

        for i in range(4):

            self.cards_frame.grid_columnconfigure(
                i,
                weight=1
            )

        # =====================================
        # Sales Summary Card
        # =====================================
        self.sales_summary = ctk.CTkFrame(
            self,
            fg_color=CARD_COLOR,
            corner_radius=FRAME_RADIUS
        )

        self.sales_summary.pack(
            fill="x",
            pady=(0, 20)
        )

        self.sales_label = ctk.CTkLabel(
            self.sales_summary,
            text="Today's Sales: Loading...",
            font=SUBTITLE_FONT,
            text_color=SUCCESS_COLOR
        )

        self.sales_label.pack(
            padx=20,
            pady=20
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

        sales = ReportService.get_sales_summary()

        self.sales_label.configure(
            text=f"Today's Sales: {sales:.2f} EGP"
        )

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

        for widget in self.cards_frame.winfo_children():
            widget.destroy()

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

        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            text_color=color
        )

        value_label.pack(
            pady=(30, 5)
        )

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

    # =====================================
    # Refresh Data
    # =====================================
    def refresh_data(self):

        self.load_statistics()

        self.generate_report()

    # =====================================
    # Export Report
    # =====================================
    def export_report(self):

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if not file_path:
            return

        report_data = self.report_box.get(
            "1.0",
            "end"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report_data)
