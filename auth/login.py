import customtkinter as ctk
from pages.dashboard import Dashboard

class LoginPage:

    def __init__(self, app):

        self.app = app

        self.frame = ctk.CTkFrame(app)
        self.frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            self.frame,
            text="LOGIN",
            font=("Arial", 35)
        )

        title.pack(pady=40)

        self.user = ctk.CTkEntry(
            self.frame,
            placeholder_text="Username",
            width=350
        )

        self.user.pack(pady=10)

        self.password = ctk.CTkEntry(
            self.frame,
            placeholder_text="Password",
            show="*",
            width=350
        )

        self.password.pack(pady=10)

        btn = ctk.CTkButton(
            self.frame,
            text="Login",
            command=self.login
        )

        btn.pack(pady=20)

    def login(self):

        self.frame.destroy()

        Dashboard(self.app)
