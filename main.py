import customtkinter as ctk
from auth.login import LoginPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1500x850")
app.title("SuperMarket POS")

LoginPage(app)

app.mainloop()
