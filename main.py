import customtkinter as ctk

from auth.login import LoginPage
from config import *
from database import db


class SuperMarketPOS(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =====================================
        # Window Configuration
        # =====================================
        self.title(APP_NAME)

        self.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.minsize(
            MIN_WIDTH,
            MIN_HEIGHT
        )

        # =====================================
        # Theme Settings
        # =====================================
        ctk.set_appearance_mode(
            APPEARANCE_MODE
        )

        ctk.set_default_color_theme(
            COLOR_THEME
        )

        # =====================================
        # Window Styling
        # =====================================
        self.configure(
            fg_color=BACKGROUND_COLOR
        )

        # =====================================
        # Close Event
        # =====================================
        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        # =====================================
        # Launch Login Page
        # =====================================
        self.current_page = LoginPage(
            self
        )

    # =====================================
    # Safe Close
    # =====================================
    def on_close(self):

        try:
            db.close()
        except:
            pass

        self.destroy()


# =====================================
# Main Function
# =====================================
def main():

    app = SuperMarketPOS()

    app.mainloop()


if __name__ == "__main__":
    main()
