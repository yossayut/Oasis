import tkinter as tk
import sqlite3

from tkinter  import ttk 
from tkinter  import messagebox, simpledialog
from datetime import datetime

from Config.Config                     import *
from Contract.CustomerRegistrationForm import RegistrationForm
from LookupAndEdit.RoomFunctions       import RoomFunctions 

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
    def change_filter(self, option):
        self.filter_var.set(option)
        self.apply_filter()

    def __init__(self, master):
        super().__init__(master)
        self.lift()
        self.title("ห้องทั้งหมด")
        self.geometry("800x500")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()
        self.bind('<Escape>', self.on_escape)

    def create_widgets(self):
        self.lift()
      
        paned_window = ttk.Panedwindow(self, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        filter_frame = ttk.Frame(paned_window)
        paned_window.add(filter_frame)

        self.filter_var = tk.StringVar(value="ห้องทั้งหมด")

        tk.Label(filter_frame, text="ห้องทั้งหมด : ").grid(row=0, column=0)                          

        ttk.Radiobutton(filter_frame, 
            text="โชว์ทั้งหมด", 
            value="Show_all_room", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_all_room")).grid(row=0, column=1, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="โชว์ห้องคนอยู่แล้ว", 
            value="Show_only_occupied_room", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_only_occupied_room")).grid(row=0, column=2, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="โชว์ห้องติดจอง", 
            value="Show_only_booked_room", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_only_booked_room")).grid(row=0, column=3, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="โชว์ห้องว่าง", 
            value="Show_free_room", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_free_room")).grid(row=0, column=4, padx=10)

        self.tree = ttk.Treeview(paned_window, 
            columns=("RoomNo", "Building", "Floor","RoomType", "Status", "CustomerID", "StartDate", "EndDate"), 
            show="headings")

        txt_room_no   = "เบอร์ห้อง"
        txt_building  = "ตึก"
        txt_floor     = "ชั้น"
        txt_room_size = "ขนาดห้อง"
        txt_status    = "สถานะ"
        txt_customer  = "ลูกค้า"
        txt_start     = "เริ่มต้น"
        txt_end       = "สิ้นสุด"

        self.tree.heading("#1", text=txt_room_no   , command=lambda: self.sort_treeview(1, True))
        self.tree.heading("#2", text=txt_building  , command=lambda: self.sort_treeview(2, True))
        self.tree.heading("#3", text=txt_floor     , command=lambda: self.sort_treeview(3, True))
        self.tree.heading("#4", text=txt_room_size , command=lambda: self.sort_treeview(4, True))
        self.tree.heading("#5", text=txt_status    , command=lambda: self.sort_treeview(5, True))
        self.tree.heading("#6", text=txt_customer  , command=lambda: self.sort_treeview(6, True))
        self.tree.heading("#7", text=txt_start     , command=lambda: self.sort_treeview(7, True))
        self.tree.heading("#8", text=txt_end       , command=lambda: self.sort_treeview(8, True))

        self.tree.column("#1",  width=10,   anchor="center")
        self.tree.column("#2",  width=10,   anchor="center")
        self.tree.column("#3",  width=10,   anchor="center")
        self.tree.column("#4",  width=40,   anchor="center")
        self.tree.column("#5",  width=40,   anchor="center")
        self.tree.column("#6",  width=40,   anchor="center")
        self.tree.column("#7",  width=40,   anchor="center")
        self.tree.column("#8",  width=40,   anchor="center")

        self.contract_button = tk.Button(self, text="เลือกห้อง", command=self.open_registration_form)
        self.contract_button.pack(pady=10)

        paned_window.add(self.tree)
        RoomFunctions.display_show_all_room(self.tree, self.filter_var)

    # Call the display_show_all_room method from RoomFunctions class
    def display_show_all_room(self):
        RoomFunctions.display_show_all_room(self.tree, self.filter_var)

    def apply_filter(self):
        self.tree.delete(*self.tree.get_children())
        RoomFunctions.display_show_all_room(self.tree, self.filter_var)

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        for index, item in enumerate(data):
            self.tree.move(item[1], '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def open_registration_form(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Room Selection", "Please select a room.")
            return
            
        self.withdraw()  # Hide the room selection
        selected_room = self.tree.item(selected_item)['values']
        selected_room = selected_room[0]

        ######################################################
        # Call RegistrationForm : CustomerRegistrationForm.py
        ######################################################
        RegistrationForm(self, selected_room)

    # Show the main page
    def on_close(self):
        self.master.deiconify()  
        self.destroy()

    # Close the current window
    def on_escape(self, event):
        self.on_close()          