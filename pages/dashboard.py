import customtkinter as ctk
from pages.products import ProductsPage
from pages.cashier import CashierPage
from pages.reports import ReportsPage

class Dashboard:

    def __init__(self, app):

        self.sidebar = ctk.CTkFrame(app, width=250)
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(app)
        self.content.pack(side="right", fill="both", expand=True)

        title = ctk.CTkLabel(
            self.sidebar,
            text="SuperMarket POS",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=30)

        buttons = [
            ("Products", self.products),
            ("Cashier", self.cashier),
            ("Reports", self.reports)
        ]

        for text, cmd in buttons:

            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=cmd,
                height=45
            )

            btn.pack(fill="x", padx=20, pady=10)

    def clear(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    def products(self):

        self.clear()

        ProductsPage(self.content)

    def cashier(self):

        self.clear()

        CashierPage(self.content)

    def reports(self):

        self.clear()

        ReportsPage(self.content)
