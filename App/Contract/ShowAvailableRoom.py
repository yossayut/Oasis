import tkinter as tk
from tkinter import ttk  # Add this line to import ttk
import sqlite3
from tkinter import messagebox, simpledialog
from datetime import datetime

from Config.Config import *
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
        self.display_show_all_room()
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

        self.tree.heading("#1", text="เบอร์ห้อง", command=lambda: self.sort_treeview(1, True))
        self.tree.heading("#2", text="ตึก",     command=lambda: self.sort_treeview(2, True))
        self.tree.heading("#3", text="ชั้น",     command=lambda: self.sort_treeview(3, True))
        self.tree.heading("#4", text="ขนาดห้อง", command=lambda: self.sort_treeview(4, True))
        self.tree.heading("#5", text="สถานะ", command=lambda: self.sort_treeview(5, True))
        self.tree.heading("#6", text="ลูกค้า", command=lambda: self.sort_treeview(6, True))
        self.tree.heading("#7", text="เริ่มต้น", command=lambda: self.sort_treeview(7, True))
        self.tree.heading("#8", text="สิ้นสุด", command=lambda: self.sort_treeview(8, True))

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
        self.display_show_all_room()

    def display_show_all_room(self):
        # Connect to the SQLite database
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            if self.filter_var.get() == "Show_all_room" :
                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'Garden view Room'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN 'จอง'
                                    ELSE '-------- ว่าง --------'
                                END AS RoomStatus,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.StartDate
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.CheckInDate
                                    ELSE '----------------'
                                END AS StartDate,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.EndDate
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.CheckOutDate
                                    ELSE '----------------'
                                END AS EndDate  

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID
                                    LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID   = Contract_TBL.CustomerID

                                    LEFT JOIN Booking_TBL  ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID
                                    LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID   = Booking_TBL.CustomerID

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;
                """)

            elif self.filter_var.get() == "Show_only_occupied_room" :
                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,
                                    CASE
                                        WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                        WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'Garden view Room'
                                        ELSE '-'
                                    END AS RoomType,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                        ELSE '-------- ว่าง --------'
                                    END AS RoomStatus,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                        ELSE '----------------'
                                    END AS CustomerName,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.StartDate
                                        ELSE '----------------'
                                    END AS StartDate,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.EndDate
                                        ELSE '----------------'
                                    END AS EndDate

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                    LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID

                                WHERE
                                    Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active'  -- Show only rooms with an active contract

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;
                """)

            elif self.filter_var.get() == "Show_only_booked_room" :
                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,
                                    CASE
                                        WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                        WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'Garden view Room'
                                        ELSE '-'
                                    END AS RoomType,

                                    CASE
                                        WHEN Booking_TBL.RoomID IS NOT NULL AND Booking_TBL.Status = 'Active' THEN 'จอง'
                                        ELSE '-------- ว่าง --------'
                                    END AS RoomStatus,

                                    CASE
                                        WHEN Booking_TBL.RoomID IS NOT NULL AND Booking_TBL.Status = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                        ELSE '----------------'
                                    END AS CustomerName,

                                    '----------------' AS StartDate,  -- Placeholder for StartDate
                                    '----------------' AS EndDate     -- Placeholder for EndDate

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Booking_TBL ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                    LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID

                                WHERE
                                    Booking_TBL.RoomID IS NOT NULL AND Booking_TBL.Status = 'Active'  -- Show only rooms with an active booking

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;

                """)

            elif self.filter_var.get() == "Show_free_room" :
                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,
                                    CASE
                                        WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                        WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'Garden view Room'
                                        ELSE '-'
                                    END AS RoomType,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                        WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN 'จอง'
                                        ELSE '-------- ว่าง --------'
                                    END AS RoomStatus,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                        WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                        ELSE '----------------'
                                    END AS CustomerName,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.StartDate
                                        WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.CheckInDate
                                        ELSE '----------------'
                                    END AS StartDate,

                                    CASE
                                        WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.EndDate
                                        WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.CheckOutDate
                                        ELSE '----------------'
                                    END AS EndDate  

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID AND Contract_TBL.Status = 'Active'
                                    LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID = Contract_TBL.CustomerID
                                    LEFT JOIN Booking_TBL ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID AND Booking_TBL.Status = 'Active'
                                    LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID = Booking_TBL.CustomerID

                                WHERE
                                    (Contract_TBL.RoomID IS NULL OR Contract_TBL.Status != 'Active') AND
                                    (Booking_TBL.RoomID IS NULL OR Booking_TBL.Status != 'Active')  -- Show only rooms without an active contract or booking

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;

                """)

            else :
                cursor.execute("""
                                SELECT
                                    Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor,

                                CASE
                                    WHEN Apartment_Info_TBL.RoomType = 'SmallType' THEN 'Standard Room'
                                    WHEN Apartment_Info_TBL.RoomType = 'BigType' THEN 'Garden view Room'
                                    ELSE '-'
                                END AS RoomType,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN 'เช่า'
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN 'จอง'
                                    ELSE '-------- ว่าง --------'
                                END AS RoomStatus,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Customer_Contract.FirstName || ' ' || Customer_Contract.LastName
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Customer_Booking.FirstName || ' ' || Customer_Booking.LastName
                                    ELSE '----------------'
                                END AS CustomerName,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.StartDate
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.CheckInDate
                                    ELSE '----------------'
                                END AS StartDate,

                                CASE
                                    WHEN Contract_TBL.RoomID IS NOT NULL AND Contract_TBL.Status = 'Active' THEN Contract_TBL.EndDate
                                    WHEN Booking_TBL.RoomID  IS NOT NULL AND Booking_TBL.Status  = 'Active' THEN Booking_TBL.CheckOutDate
                                    ELSE '----------------'
                                END AS EndDate  

                                FROM
                                    Apartment_Info_TBL
                                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID
                                    LEFT JOIN Customer_TBL AS Customer_Contract ON Customer_Contract.CustomerID   = Contract_TBL.CustomerID

                                    LEFT JOIN Booking_TBL  ON Apartment_Info_TBL.RoomID = Booking_TBL.RoomID
                                    LEFT JOIN Customer_TBL AS Customer_Booking ON Customer_Booking.CustomerID   = Booking_TBL.CustomerID

                                ORDER BY
                                    Apartment_Info_TBL.RoomNo;
                """)

            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                background_color = "light gray" if i % 2 == 0 else "white"
                self.tree.tag_configure(f"row{i}", background=background_color)
                self.tree.insert("", "end", values=row, tags=(f"row{i}"))

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()

    def apply_filter(self):
        self.tree.delete(*self.tree.get_children())
        self.display_show_all_room()

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        for index, item in enumerate(data):
            self.tree.move(item[1], '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def open_registration_form(self):
        selected_item = self.tree.selection()
        if DEBUG == True :
            print(selected_item)

        if not selected_item:
            messagebox.showwarning("Room Selection", "Please select a room.")
            return
        self.withdraw()  # Hide the room selection

        selected_room = self.tree.item(selected_item)['values']
        if DEBUG == True :
            print(selected_room)
            
        selected_room = selected_room[0]
        ######################################################
        # Call RegistrationForm : CustomerRegistrationForm.py
        ######################################################
        if DEBUG == True :
            print(selected_room)

        RegistrationForm(self, selected_room)

    def on_close(self):
        self.master.deiconify()  # Show the main page
        self.destroy()

    def on_escape(self, event):
        self.on_close()          # Close the current window