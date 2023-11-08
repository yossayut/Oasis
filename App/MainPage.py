import tkinter as tk
import sqlite3

from tkinter              import messagebox, simpledialog
from datetime             import datetime

from Config.Config                import *
from Contract.ShowAvailableRoom   import CheckAvailableRoomPage

# from Parking              import ParkingPage
# from Requistition         import RequisitionPage
from KeyCard.Keycard                 import KeycardPage
from Interested.InterestedPerson     import InterestedPersonPage
# from Internet             import InternetPage
from LookupAndEdit.LookupEdit        import LookUpAndEditPage

#############################################################################################################
# Main page contain button : ทำสัญญาเช่าห้องพัก, ที่จอดรถ, เบิกของ, ลงทะเบียนผู้สนใจ,ดูหรือแก้ไขข้อมูล
# if click each button it will navigate to list of selected window
#############################################################################################################
class MainPage(tk.Tk):
    # 1 : Initial Window
    def __init__(self):
        super().__init__()
        self.title("Main Page")
        self.geometry("600x400")
        self.create_main_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # Bind the window close event to a function

    # 2 : Create widgets(Button) from Initial Window
    def create_main_widgets(self):
        tk.Label(self, text="Main Page", font=("Arial", 18)).pack(pady=20)
        
        contract_txt    = "ทำสัญญาเช่าห้องพัก"
        parking_txt     = "ที่จอดรถ"
        internet_txt    = "อินเตอร์เน็ต"
        keycard_txt     = "คีย์การ์ด"
        interest_txt    = "ลงทะเบียนผู้สนใจ"
        lookup_txt      = "ดูหรือแก้ไขข้อมูล"

        tk.Button(self, text=contract_txt    , command=self.open_create_contract).pack(pady=10)
        tk.Button(self, text=keycard_txt     , command=self.open_keycard).pack(pady=10)
        tk.Button(self, text=parking_txt     , command=self.open_parking).pack(pady=10)
        tk.Button(self, text=internet_txt    , command=self.open_internet).pack(pady=10)
        tk.Button(self, text=interest_txt    , command=self.open_interested_person).pack(pady=10)
        tk.Button(self, text=lookup_txt      , command=self.open_lookup_edit).pack(pady=10)
    
    # 3 : Click open_check_room from main page  
    def open_create_contract(self):
        self.withdraw()
        self.lift()
        CheckAvailableRoomPage(self)

    # # 6 : Click open_requisition from main page   
    def open_keycard(self):
        self.withdraw()
        KeycardPage(self)

    # 4 : Click open_parking from main page    
    def open_parking(self):
        self.withdraw()
    #     ParkingPage(self)

    # # 5 : Click open_parking from main page    
    def open_internet(self):
        self.withdraw()
    #     InternetPage(self)


    # # 7 : Click open_interested_person from main page   
    def open_interested_person(self):
        self.withdraw()
        InterestedPersonPage(self)

    # # 8 : Click open_lookup_edit from main page   
    def open_lookup_edit(self):
        if DEBUG == True :
            print("MainPage : open_lookup_edit")
            
        self.withdraw()
        LookUpAndEditPage(self)

    # 9
    def on_close(self):
        self.destroy()


#############################################################################################################
# MAIN
#############################################################################################################
if __name__ == "__main__":
    app = MainPage()
    app.mainloop()
