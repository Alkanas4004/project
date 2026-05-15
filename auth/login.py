# auth/login.py

import customtkinter as ctk

from pages.dashboard import Dashboard
from database import cursor
from config import *


class LoginPage:

    def __init__(self, app):

        self.app = app

        # =========================
        # Main Background
        # =========================
        self.frame = ctk.CTkFrame(
            app,
            fg_color=BACKGROUND_COLOR
        )

        self.frame.pack(fill="both", expand=True)

        # =========================
        # Login Card
        # =========================
        self.card = ctk.CTkFrame(
            self.frame,
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

        # =========================
        # App Title
        # =========================
        title = ctk.CTkLabel(
            self.card,
            text=APP_NAME,
            font=TITLE_FONT,
            text_color=TEXT_COLOR
        )

        title.pack(pady=(40, 10))

        # =========================
        # Subtitle
        # =========================
        subtitle = ctk.CTkLabel(
            self.card,
            text="Login To Continue",
            font=TEXT_FONT,
            text_color=TEXT_SECONDARY
        )

        subtitle.pack(pady=(0, 30))

        # =========================
        # Username Entry
        # =========================
        self.user = ctk.CTkEntry(
            self.card,
            placeholder_text="Username",
            width=350,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.user.pack(pady=10)

        # =========================
        # Password Entry
        # =========================
        self.password = ctk.CTkEntry(
            self.card,
            placeholder_text="Password",
            show="●",
            width=350,
            height=ENTRY_HEIGHT,
            corner_radius=BUTTON_RADIUS,
            font=TEXT_FONT
        )

        self.password.pack(pady=10)

        # =========================
        # Login Button
        # =========================
        login_btn = ctk.CTkButton(
            self.card,
            text="LOGIN",
            width=350,
            height=50,
            corner_radius=BUTTON_RADIUS,
            fg_color=PRIMARY_COLOR,
            hover_color="#1D4ED8",
            font=BUTTON_FONT,
            command=self.login
        )

        login_btn.pack(pady=25)

        # =========================
        # Status Label
        # =========================
        self.status = ctk.CTkLabel(
            self.card,
            text="",
            font=SMALL_FONT,
            text_color=DANGER_COLOR
        )

        self.status.pack(pady=5)

        # =========================
        # Footer
        # =========================
        footer = ctk.CTkLabel(
            self.card,
            text="© 2026 SuperMarket POS",
            font=SMALL_FONT,
            text_color=TEXT_SECONDARY
        )

        footer.pack(side="bottom", pady=20)

    # =========================
    # Login Function
    # =========================
    def login(self):

        username = self.user.get().strip()
        password = self.password.get().strip()

        # Empty Fields Validation
        if not username or not password:

            self.status.configure(
                text="Please enter username and password"
            )

            return

        # Database Check
        cursor.execute(
            """
            SELECT * FROM users
            WHERE username=? AND password=?
            """,
            (username, password)
        )

        user = cursor.fetchone()

        # Success Login
        if user:

            self.frame.destroy()

            Dashboard(self.app)

        # Failed Login
        else:

            self.status.configure(
                text="Invalid username or password"
            )
