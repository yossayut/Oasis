import tkinter as tk
from tkinter import ttk
import sqlite3
from Config.Config                import *

class Show_keycard_Page(tk.Toplevel):
    def change_filter(self, option):
        self.filter_var.set(option)
        self.apply_filter()

    def __init__(self, master):
        super().__init__(master)
        self.title("ห้องพักทั้งหมด")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()

    def create_widgets(self):
        paned_window = ttk.Panedwindow(self, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        filter_frame = ttk.Frame(paned_window)
        paned_window.add(filter_frame)

        self.filter_var = tk.StringVar(value="ห้องทั้งหมด")

        ttk.Radiobutton(filter_frame, 
            text="ห้องทั้งหมด", 
            value="Show all", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show all")).grid(row=0, column=0, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="เฉพาะห้องที่ว่าง", 
            value="Free rooms", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Free rooms")).grid(row=0, column=1, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="เฉพาะห้องเช่าแล้ว", 
            value="Rent rooms", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Rent rooms")).grid(row=0, column=2, padx=10)

        ttk.Radiobutton(filter_frame, 
        	text="ทั้งหมดเรียงตามผู้เช่า", 
        	value="Rent rooms order by customer", 
        	variable=self.filter_var, 
        	command=lambda: self.change_filter("Rent rooms order by customer")).grid(row=0, column=3, padx=10)

        self.tree = ttk.Treeview(paned_window, 
        	columns=("Room ID", "Room Number", "Building", "Floor", "Room Type", "Rent", "Start Date", "End Date"), 
        	show="headings")

        self.tree.heading("#1", text="ลำดับที่", command=lambda: self.sort_treeview(1, True))
        self.tree.heading("#2", text="เบอร์ห้อง", command=lambda: self.sort_treeview(2, True))
        self.tree.heading("#3", text="อาคาร", command=lambda: self.sort_treeview(3, True))
        self.tree.heading("#4", text="ชั้น",    command=lambda: self.sort_treeview(4, True))
        self.tree.heading("#5", text="ขนาดห้อง", command=lambda: self.sort_treeview(5, True))
        self.tree.heading("#6", text="เช่า", command=lambda: self.sort_treeview(6, True))
        self.tree.heading("#7", text="เริ่มต้น", command=lambda: self.sort_treeview(7, True))
        self.tree.heading("#8", text="สิ้นสุด", command=lambda: self.sort_treeview(8, True))

        self.tree.column("#1", width=40,  anchor="center")
        self.tree.column("#2", width=80,  anchor="center")
        self.tree.column("#3", width=80,  anchor="center")
        self.tree.column("#4", width=60,  anchor="center")
        self.tree.column("#5", width=80,  anchor="center")
        self.tree.column("#6", width=150, anchor="center")
        self.tree.column("#7", width=80,  anchor="center")
        self.tree.column("#8", width=80,  anchor="center")

        paned_window.add(self.tree)
        self.display_show_all_room()

    def display_show_all_room(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            if self.filter_var.get() == "Free rooms":
                # Select only free rooms
                cursor.execute("""
                    SELECT Apartment_Info_TBL.RoomID, Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor, Apartment_Info_TBL.RoomType,
                    '', '', '', ''
                    FROM Apartment_Info_TBL
                    WHERE Apartment_Info_TBL.RoomID NOT IN (SELECT RoomID FROM Contract_TBL WHERE Status = 'Active')
                    ORDER BY Apartment_Info_TBL.RoomID
                """)

            elif self.filter_var.get() == "Rent rooms":
                # Select only rent rooms
                cursor.execute("""
                    SELECT Apartment_Info_TBL.RoomID, Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor, Apartment_Info_TBL.RoomType,
                    CASE WHEN Contract_TBL.Status = 'Active' THEN Customer_TBL.FirstName || ' ' || Customer_TBL.LastName ELSE '' END AS Rent,
                    COALESCE(Contract_TBL.StartDate, ''), COALESCE(Contract_TBL.EndDate, '')
                    FROM Apartment_Info_TBL
                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID
                    LEFT JOIN Customer_TBL ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    WHERE Contract_TBL.Status = 'Active'
                    ORDER BY Apartment_Info_TBL.RoomID
                """)

            elif self.filter_var.get() == "Rent rooms order by customer":
                # Select only rent rooms order by customer name
                cursor.execute("""
                    SELECT Apartment_Info_TBL.RoomID, Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor, Apartment_Info_TBL.RoomType,
                    CASE WHEN Contract_TBL.Status = 'Active' THEN Customer_TBL.FirstName || ' ' || Customer_TBL.LastName ELSE '' END AS Rent,
                    COALESCE(Contract_TBL.StartDate, ''), COALESCE(Contract_TBL.EndDate, '')
                    FROM Apartment_Info_TBL
                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID
                    LEFT JOIN Customer_TBL ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    WHERE Contract_TBL.Status = 'Active'
                    ORDER BY Customer_TBL.FirstName
                """)

            else:
                # Show all rooms
                cursor.execute("""
                    SELECT Apartment_Info_TBL.RoomID, Apartment_Info_TBL.RoomNo, Apartment_Info_TBL.Building, Apartment_Info_TBL.Floor, Apartment_Info_TBL.RoomType,
                    CASE WHEN Contract_TBL.Status = 'Active' THEN Customer_TBL.FirstName || ' ' || Customer_TBL.LastName ELSE '' END AS Rent,
                    COALESCE(Contract_TBL.StartDate, ''), COALESCE(Contract_TBL.EndDate, '')
                    FROM Apartment_Info_TBL
                    LEFT JOIN Contract_TBL ON Apartment_Info_TBL.RoomID = Contract_TBL.RoomID
                    LEFT JOIN Customer_TBL ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    ORDER BY Apartment_Info_TBL.RoomID
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

    def on_close(self):
        self.master.deiconify()  # Show the main page
        self.destroy()