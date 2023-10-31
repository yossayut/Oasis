import tkinter as tk
import sqlite3
from tkinter  import messagebox, simpledialog
from datetime import datetime

from Config.Config                     import *
from Contract.CustomerRegistrationForm import RegistrationForm  

#############################################################################################################
# Create ParkingPage, It will show the available parking from Database and if select,
# it will go to the register form
#  CheckRoomPage 
#    -> create_widgets_check_room_contract
#        -> open_registration_form
#            -> RegistrationForm
#                -> submit_form
#                    -> clear_form
#    -> display_available_rooms
#############################################################################################################
class CheckAvailableRoomPage(tk.Toplevel):
    # 1
    def __init__(self, master):
        super().__init__(master)
        self.lift()
        self.title("ห้องว่าง")
        self.geometry("300x300")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()
        self.display_available_rooms()
        self.bind('<Escape>', self.on_escape)

    # 2
    def create_widgets(self):
        self.lift()
        self.rooms_listbox   = tk.Listbox(self)
        self.rooms_listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.contract_button = tk.Button(self, text="เลือกห้อง", command=self.open_registration_form)
        self.contract_button.pack(pady=10)

    # 3
    def display_available_rooms(self):
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()
        try:
            # Select available rooms from the table where there is no active contract for the room
            cursor.execute( """
                                SELECT    Apartment_Info_TBL.RoomNo
                                FROM      Apartment_Info_TBL
                                LEFT JOIN Contract_TBL
                                ON        Apartment_Info_TBL.RoomID = Contract_TBL.RoomID
                                WHERE     Contract_TBL.Status IS NULL     OR  
                                          Contract_TBL.Status = 'Expired' OR
                                          Contract_TBL.Status = 'Quit';
                            """)
            rows = cursor.fetchall()

            for row in rows:
                self.rooms_listbox.insert(tk.END, row[0])

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()   # Close the database connection

    # 4
    def open_registration_form(self):
        selected_room = self.rooms_listbox.get(tk.ACTIVE)

        if not selected_room:
            messagebox.showwarning("Room Selection", "Please select a room.")
            return
        self.withdraw()  # Hide the room selection

        ######################################################
        # Call RegistrationForm : CustomerRegistrationForm.py
        ######################################################
        RegistrationForm(self, selected_room)

    # 5
    def on_close(self):
        self.master.deiconify()  # Show the main page
        self.destroy()

    # 6
    def on_escape(self, event):
        self.on_close()          # Close the current window