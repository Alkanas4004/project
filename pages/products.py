import customtkinter as ctk
from database import conn, cursor

class ProductsPage:

    def __init__(self, parent):

        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True)

        self.name = ctk.CTkEntry(frame, placeholder_text="Product Name")
        self.name.pack(pady=5)

        self.barcode = ctk.CTkEntry(frame, placeholder_text="Barcode")
        self.barcode.pack(pady=5)

        self.buy = ctk.CTkEntry(frame, placeholder_text="Buy Price")
        self.buy.pack(pady=5)

        self.sell = ctk.CTkEntry(frame, placeholder_text="Sell Price")
        self.sell.pack(pady=5)

        self.qty = ctk.CTkEntry(frame, placeholder_text="Quantity")
        self.qty.pack(pady=5)

        btn = ctk.CTkButton(
            frame,
            text="Save Product",
            command=self.save
        )

        btn.pack(pady=10)

        self.box = ctk.CTkTextbox(frame, width=1000, height=400)
        self.box.pack(pady=20)

        self.load()

    def save(self):

        cursor.execute(
            '''
            INSERT INTO products(
                name,barcode,buy_price,sell_price,quantity
            )
            VALUES(?,?,?,?,?)
            ''',
            (
                self.name.get(),
                self.barcode.get(),
                self.buy.get(),
                self.sell.get(),
                self.qty.get()
            )
        )

        conn.commit()

        self.load()

    def load(self):

        self.box.delete("1.0", "end")

        cursor.execute("SELECT * FROM products")

        for product in cursor.fetchall():

            self.box.insert(
                "end",
                f"{product[1]} | {product[4]} EGP | Qty:{product[5]}\n"
            )
