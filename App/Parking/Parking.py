import tkinter as tk
import sqlite3

from tkinter  import ttk, messagebox, simpledialog # Add this line to import ttk
from datetime import datetime

from Config.Config                     import *
from Parking.ParkingRegistrationForm   import ParkingRegistrationForm
from LookupAndEdit.ParkFunctions       import ParkFunctions 

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
class ParkingPage(tk.Toplevel):
    def change_filter(self, option):
        self.filter_var.set(option)
        self.apply_filter()

    def __init__(self, master):
        super().__init__(master)
        self.lift()
        self.title("รถทั้งหมด")
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

        self.filter_var = tk.StringVar(value="รถทั้งหมด")

        tk.Label(filter_frame, text="รถทั้งหมด : ").grid(row=0, column=0)                          

        ttk.Radiobutton(filter_frame, 
            text="โชว์ห้องทั้งหมด", 
            value="Show_all_car", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_all_room")).grid(row=0, column=1, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="โชว์เฉพาะห้องที่จอด", 
            value="Show_only_parked_room", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_only_parked_room")).grid(row=0, column=2, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="โชว์เฉพาะมอเตอร์ไซค์", 
            value="Show_only_room_have_bike", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_only_room_have_bike")).grid(row=0, column=3, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="โชว์เฉพาะรถยนต์", 
            value="Show_only_room_have_car", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_only_room_have_car")).grid(row=0, column=4, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="โชว์ห้องที่ยังไม่จอด", 
            value="Show_free_room", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_free_room")).grid(row=0, column=5, padx=10)

        self.tree = ttk.Treeview(paned_window, 
            columns=("RoomNo", "Building", "Floor","RoomType", "CustomerID", "Type", "Brand","Color","PlateNo"), 
            show="headings")

        txt_room_no       = "เบอร์ห้อง"
        txt_building      = "ตึก"
        txt_floor         = "ชั้น"
        txt_room_size     = "ขนาดห้อง"
        txt_customer_name = "ชื่อนามสกุลลูกค้า"
        txt_venhicle_type = "ประเภท"
        txt_brand         = "ยี่ห้อ/รุ่น"
        txt_color         = "สี"
        txt_plate_no      = "ทะเบียน"
        txt_add           = "เพิ่มจอดรถ/มอไซต์"  

        self.tree.heading("#1", text=txt_room_no        ,   command=lambda: self.sort_treeview(1, True))
        self.tree.heading("#2", text=txt_building       ,   command=lambda: self.sort_treeview(2, True))
        self.tree.heading("#3", text=txt_floor          ,   command=lambda: self.sort_treeview(3, True))
        self.tree.heading("#4", text=txt_room_size      ,   command=lambda: self.sort_treeview(4, True))
        self.tree.heading("#5", text=txt_customer_name  ,   command=lambda: self.sort_treeview(5, True))
        self.tree.heading("#6", text=txt_venhicle_type  ,   command=lambda: self.sort_treeview(6, True))
        self.tree.heading("#7", text=txt_brand          ,   command=lambda: self.sort_treeview(7, True))
        self.tree.heading("#8", text=txt_color          ,   command=lambda: self.sort_treeview(8, True))
        self.tree.heading("#9", text=txt_plate_no       ,   command=lambda: self.sort_treeview(9, True))

        self.tree.column("#1",  width=10,   anchor="center")
        self.tree.column("#2",  width=10,   anchor="center")
        self.tree.column("#3",  width=10,   anchor="center")
        self.tree.column("#4",  width=40,   anchor="center")
        self.tree.column("#5",  width=40,   anchor="center")
        self.tree.column("#6",  width=40,   anchor="center")
        self.tree.column("#7",  width=40,   anchor="center")
        self.tree.column("#8",  width=40,   anchor="center")
        self.tree.column("#9",  width=40,   anchor="center")

        self.parking_button = tk.Button(self, text=txt_add , command=self.open_parking_registration_form)
        self.parking_button.pack(pady=10)

        paned_window.add(self.tree)
       
        ParkFunctions.display_show_all_parking(self.tree, self.filter_var)

    # Call the display_show_all_room method from ParkFunctions class
    def display_show_all_parking(self):
        ParkFunctions.display_show_all_parking(self.tree, self.filter_var)

    def apply_filter(self):
        self.tree.delete(*self.tree.get_children())
        ParkFunctions.display_show_all_parking(self.tree, self.filter_var)

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        for index, item in enumerate(data):
            self.tree.move(item[1], '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def open_parking_registration_form(self):
        selected_item     = self.tree.selection()

        if not selected_item:
            messagebox.showwarning("Room Selection", "Please select a room.")
            return

        self.withdraw()  
        selected_room     = self.tree.item(selected_item)['values']
        selected_customer = selected_room[4]

        ParkingRegistrationForm(self, selected_customer)

        if DEBUG == True :
            print("open_parking_registration_form => selected_room     : " , selected_room)
            print("open_parking_registration_form => selected_item     : " , selected_item)
            print("open_parking_registration_form => selected_customer : " , selected_customer)

    def on_close(self):
        self.master.deiconify()  # Show the main page
        self.destroy()

    def on_escape(self, event):
        self.on_close()          # Close the current window