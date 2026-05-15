import customtkinter as ctk

from pages.dashboard import DashboardPage
from services.auth_service import AuthService

from config import *


class LoginPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.master = master

        self.pack(fill="both", expand=True)

        self.build_ui()

    # =====================================
    # UI
    # =====================================
    def build_ui(self):

        # Main Container
        self.configure(
            fg_color=BACKGROUND_COLOR
        )

        # =====================================
        # Login Card
        # =====================================
        self.card = ctk.CTkFrame(
            self,
            width=450,
            height=520,
            corner_radius=FRAME_RADIUS,
            fg_color=CARD_COLOR
        )

        self.card.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        # =====================================
        # Logo / Title
        # =====================================
        self.title = ctk.CTkLabel(
            self.card,
            text=APP_NAME,
            font=TITLE_FONT,
            text_color=TEXT_COLOR
        )

        self.title.pack(
            pady=(40, 10)
        )

        # =====================================
        # Subtitle
        # =====================================
        self.subtitle = ctk.CTkLabel(
            self.card,
            text="Login To Continue",
            font=TEXT_FONT,
            text_color=TEXT_SECONDARY
        )

        self.subtitle.pack(
            pady=(0, 30)
        )

        # =====================================
        # Username Entry
        # =====================================
        self.username_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Username",
            width=350,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.username_entry.pack(
            pady=10
        )

        # =====================================
        # Password Entry
        # =====================================
        self.password_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Password",
            show="●",
            width=350,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.password_entry.pack(
            pady=10
        )

        # =====================================
        # Login Button
        # =====================================
        self.login_button = ctk.CTkButton(
            self.card,
            text="LOGIN",
            width=350,
            height=50,
            corner_radius=BUTTON_RADIUS,
            fg_color=PRIMARY_COLOR,
            hover_color=PRIMARY_HOVER,
            font=BUTTON_FONT,
            command=self.login
        )

        self.login_button.pack(
            pady=25
        )

        # =====================================
        # Status Label
        # =====================================
        self.status_label = ctk.CTkLabel(
            self.card,
            text="",
            font=SMALL_FONT,
            text_color=DANGER_COLOR
        )

        self.status_label.pack(
            pady=5
        )

        # =====================================
        # Footer
        # =====================================
        self.footer = ctk.CTkLabel(
            self.card,
            text="© 2026 SuperMarket POS",
            font=SMALL_FONT,
            text_color=TEXT_SECONDARY
        )

        self.footer.pack(
            side="bottom",
            pady=20
        )

        # =====================================
        # Enter Key Login
        # =====================================
        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

    # =====================================
    # Login Function
    # =====================================
    def login(self):

        username = self.username_entry.get().strip()

        password = self.password_entry.get().strip()

        # Empty Validation
        if not username or not password:

            self.show_error(
                "Please enter username and password"
            )

            return

        # Disable Button While Loading
        self.login_button.configure(
            state="disabled",
            text="Please Wait..."
        )

        # Authentication
        user = AuthService.login(
            username,
            password
        )

        # Success
        if user:

            self.destroy()

            DashboardPage(
                self.master,
                user
            )

        # Failed
        else:

            self.show_error(
                "Invalid username or password"
            )

        # Enable Button Again
        self.login_button.configure(
            state="normal",
            text="LOGIN"
        )

    # =====================================
    # Error Handler
    # =====================================
    def show_error(self, message):

        self.status_label.configure(
            text=message
        )

        # Failed Login
        else:

            self.status.configure(
                text="Invalid username or password"
            )
