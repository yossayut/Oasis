import tkinter as tk
from LookupAndEdit.ShowAllRoom     import Show_all_room_Page
from LookupAndEdit.ShowAllContract import Show_all_contract_Page
from LookupAndEdit.ShowKeycard     import Show_keycard_Page

class LookUpAndEditPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Lookup Page")
        self.geometry("600x400")
        self.create_main_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_main_widgets(self):
        tk.Label(self, text="Lookup Page", font=("Arial", 18)).pack(pady=20)

        txt_show_all_room     = "ห้องพักทั้งหมด"
        txt_show_all_contract = "สัญญาเช่าทั้งหมด"
        txt_show_keycard      = "คีย์การ์ดทั้งหมด"

        tk.Button(self, text=txt_show_all_room     , command=self.show_all_room).pack(pady=10)        
        tk.Button(self, text=txt_show_all_contract , command=self.show_all_contract).pack(pady=10)
        tk.Button(self, text=txt_show_keycard      , command=self.show_keycard).pack(pady=10)
        
    def show_all_room(self):
        self.withdraw()
        Show_all_room_Page(self)

    def show_all_contract(self):
        self.withdraw()
        Show_all_contract_Page(self)

    def show_keycard(self):
        self.withdraw()
        Show_keycard_Page(self)

    def on_close(self):
        self.master.deiconify()  # Show the main page
        self.destroy()
