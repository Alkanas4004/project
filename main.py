import customtkinter as ctk
from auth.login import LoginPage


class SuperMarketPOS(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("SuperMarket POS System")
        self.geometry("1600x900")
        self.minsize(1200, 700)

        # Theme Settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Colors
        self.bg_color = "#0F172A"

        # Window Styling
        self.configure(fg_color=self.bg_color)

        # Launch Login Page
        LoginPage(self)


def main():

    app = SuperMarketPOS()

    app.mainloop()


if __name__ == "__main__":
    main()
