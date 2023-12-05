import tkinter as tk
import sqlite3

from tkinter                        import messagebox, simpledialog
from datetime                       import datetime

from Config.Config                  import *
from Contract.ShowAvailableRoom     import CheckAvailableRoomPage
from Parking.Parking                import ParkingPage
from KeyCard.Keycard                import KeycardPage
from Interested.InterestedPerson    import InterestedPersonPage
from LookupAndEdit.LookupEdit       import LookUpAndEditPage
# from Internet                       import InternetPage
# from Requistition                   import RequisitionPage
#############################################################################################################
# Main page contain button : ทำสัญญาเช่าห้องพัก, ที่จอดรถ, เบิกของ, ลงทะเบียนผู้สนใจ,ดูหรือแก้ไขข้อมูล
# if click each button it will navigate to list of selected window
#############################################################################################################
class MainPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Page")
        self.geometry("600x400")
        self.create_main_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Bind the window close event to a function

    def create_main_widgets(self):
        tk.Label(self, text="Main Page", font=("Arial", 18)).pack(pady=20)
        
        contract_txt    = "ทำสัญญาเช่า/จองห้องพัก"
        parking_txt     = "ที่จอดรถ"
        # internet_txt    = "อินเตอร์เน็ต"
        keycard_txt     = "คีย์การ์ด"
        interest_txt    = "ลงทะเบียนผู้สนใจ"
        lookup_txt      = "ดูหรือแก้ไขข้อมูล"

        tk.Button(self, text=contract_txt    , command=self.open_create_contract).pack(pady=10)
        tk.Button(self, text=keycard_txt     , command=self.open_keycard).pack(pady=10)
        tk.Button(self, text=parking_txt     , command=self.open_parking).pack(pady=10)
        # tk.Button(self, text=internet_txt    , command=self.open_internet).pack(pady=10)
        tk.Button(self, text=interest_txt    , command=self.open_interested_person).pack(pady=10)
        tk.Button(self, text=lookup_txt      , command=self.open_lookup_edit).pack(pady=10)
    
    def open_create_contract(self):
        self.withdraw()
        self.lift()
        CheckAvailableRoomPage(self)
 
    def open_keycard(self):
        self.withdraw()
        KeycardPage(self)
   
    def open_parking(self):
        self.withdraw()
        ParkingPage(self)
  
    # def open_internet(self):
    #     self.withdraw()
    # #     InternetPage(self)
 
    def open_interested_person(self):
        self.withdraw()
        InterestedPersonPage(self)

    def open_lookup_edit(self):
        self.withdraw()
        LookUpAndEditPage(self)

    def on_close(self):
        self.destroy()

#############################################################################################################
# MAIN
#############################################################################################################
if __name__ == "__main__":
    app = MainPage()
    app.mainloop()
