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
        self.title("บัตรคีย์การ์ดทั้งหมด")
        self.geometry("800x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()

    def create_widgets(self):
        paned_window = ttk.Panedwindow(self, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        filter_frame = ttk.Frame(paned_window)
        paned_window.add(filter_frame)

        self.filter_var = tk.StringVar(value="บัตรคีย์การ์ดทั้งหมด")

        ttk.Radiobutton(filter_frame, 
            text="บัตรคีย์การ์ดทั้งหมด", 
            value="Show all", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show all")).grid(row=0, column=0, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="บัตรคีย์การ์ดที่ว่าง", 
            value="Free keycard", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Free keycard")).grid(row=0, column=1, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="เฉพาะบัตรคีย์การ์ดที่ถูกใช้", 
            value="Used keycard", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Used keycard")).grid(row=0, column=2, padx=10)

        ttk.Radiobutton(filter_frame, 
        	text="ทั้งหมดเรียงตามผู้เช่า", 
        	value="Used keycard order by RoomNo", 
        	variable=self.filter_var, 
        	command=lambda: self.change_filter("Used keycard order by RoomNo")).grid(row=0, column=3, padx=10)

        self.tree = ttk.Treeview(paned_window, 
        	columns=("Keycard No.", "Keycard ID", "Customer First Name Last Name", "Customer Room", "Staff First Name Last Name", "Status"), 
        	show="headings")

        self.tree.heading("#1", text="เลขที่บัตร", command=lambda: self.sort_treeview(1, True))
        self.tree.heading("#2", text="ID บัตร", command=lambda: self.sort_treeview(2, True))
        self.tree.heading("#3", text="ชื่อนามสกุลลูกค้า", command=lambda: self.sort_treeview(3, True))
        self.tree.heading("#4", text="ห้อง", command=lambda: self.sort_treeview(4, True))
        self.tree.heading("#5", text="ชื่อนามสกุลพนักงาน", command=lambda: self.sort_treeview(5, True))
        self.tree.heading("#6", text="สถานะบัตร", command=lambda: self.sort_treeview(6, True))

        self.tree.column("#1", width=40,  anchor="center")
        self.tree.column("#2", width=80,  anchor="center")
        self.tree.column("#3", width=80,  anchor="center")
        self.tree.column("#4", width=60,  anchor="center")
        self.tree.column("#5", width=80,  anchor="center")
        self.tree.column("#6", width=150, anchor="center")

        paned_window.add(self.tree)
        self.display_show_all_keycard()

    def display_show_all_keycard(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            if self.filter_var.get() == "Free keycard":
                cursor.execute("""
                    SELECT 
                        Access_Card_Manage_TBL.ID, 
                        COALESCE(Access_Card_Manage_TBL.KeycardID, '-') AS KeycardID,
                        COALESCE(Customer_TBL.FirstName || ' ' || Customer_TBL.LastName, '-') AS CustomerName,
                        COALESCE(Apartment_Info_TBL.RoomNo, '-') AS RoomNo,
                        COALESCE(Employee_TBL.FirstName || ' ' || Employee_TBL.LastName, '-') AS EmployeeName,
                        CASE 
                            WHEN Access_Card_Manage_TBL.Status = 'Idle' THEN 'ว่าง'
                            WHEN Access_Card_Manage_TBL.Status = 'Used' THEN 'ใช้งานอยู่'
                            ELSE '-'
                        END AS Status  
                    FROM Access_Card_Manage_TBL
                    LEFT JOIN Customer_TBL ON Access_Card_Manage_TBL.CustomerID = Customer_TBL.CustomerID
                    LEFT JOIN Contract_TBL ON Customer_TBL.CustomerID = Contract_TBL.CustomerID
                    LEFT JOIN Apartment_Info_TBL ON Contract_TBL.RoomID = Apartment_Info_TBL.RoomID
                    LEFT JOIN Employee_TBL ON Access_Card_Manage_TBL.StaffID = Employee_TBL.EmployeeID
                    WHERE Access_Card_Manage_TBL.Status = 'Idle'
                    ORDER BY Access_Card_Manage_TBL.ID;
                """)

            elif self.filter_var.get() == "Used keycard":
                cursor.execute("""
                    SELECT 
                        Access_Card_Manage_TBL.ID, 
                        COALESCE(Access_Card_Manage_TBL.KeycardID, '-') AS KeycardID,
                        COALESCE(Customer_TBL.FirstName || ' ' || Customer_TBL.LastName, '-') AS CustomerName,
                        COALESCE(Apartment_Info_TBL.RoomNo, '-') AS RoomNo,
                        COALESCE(Employee_TBL.FirstName || ' ' || Employee_TBL.LastName, '-') AS EmployeeName,
                        CASE 
                            WHEN Access_Card_Manage_TBL.Status = 'Idle' THEN 'ว่าง'
                            WHEN Access_Card_Manage_TBL.Status = 'Used' THEN 'ใช้งานอยู่'
                            ELSE '-'
                        END AS Status  
                    FROM Access_Card_Manage_TBL
                    LEFT JOIN Customer_TBL ON Access_Card_Manage_TBL.CustomerID = Customer_TBL.CustomerID
                    LEFT JOIN Contract_TBL ON Customer_TBL.CustomerID = Contract_TBL.CustomerID
                    LEFT JOIN Apartment_Info_TBL ON Contract_TBL.RoomID = Apartment_Info_TBL.RoomID
                    LEFT JOIN Employee_TBL ON Access_Card_Manage_TBL.StaffID = Employee_TBL.EmployeeID
                    WHERE Access_Card_Manage_TBL.Status = 'Used'
                    ORDER BY Access_Card_Manage_TBL.ID;
                """)

            elif self.filter_var.get() == "Used keycard order by RoomNo":
                cursor.execute("""
                    SELECT 
                        Access_Card_Manage_TBL.ID, 
                        COALESCE(Access_Card_Manage_TBL.KeycardID, '-') AS KeycardID,
                        COALESCE(Customer_TBL.FirstName || ' ' || Customer_TBL.LastName, '-') AS CustomerName,
                        COALESCE(Apartment_Info_TBL.RoomNo, '-') AS RoomNo,
                        COALESCE(Employee_TBL.FirstName || ' ' || Employee_TBL.LastName, '-') AS EmployeeName,
                        CASE 
                            WHEN Access_Card_Manage_TBL.Status = 'Idle' THEN 'ว่าง'
                            WHEN Access_Card_Manage_TBL.Status = 'Used' THEN 'ใช้งานอยู่'
                            ELSE '-'
                        END AS Status  
                    FROM Access_Card_Manage_TBL
                    LEFT JOIN Customer_TBL ON Access_Card_Manage_TBL.CustomerID = Customer_TBL.CustomerID
                    LEFT JOIN Contract_TBL ON Customer_TBL.CustomerID = Contract_TBL.CustomerID
                    LEFT JOIN Apartment_Info_TBL ON Contract_TBL.RoomID = Apartment_Info_TBL.RoomID
                    LEFT JOIN Employee_TBL ON Access_Card_Manage_TBL.StaffID = Employee_TBL.EmployeeID
                    WHERE Access_Card_Manage_TBL.Status = 'Used' AND Customer_TBL.FirstName IS NOT NULL AND Customer_TBL.LastName IS NOT NULL
                    ORDER BY Apartment_Info_TBL.RoomNo;
                """)

            else:
                # Show all KeyCard
                cursor.execute("""
                    SELECT 
                        Access_Card_Manage_TBL.ID, 
                        COALESCE(Access_Card_Manage_TBL.KeycardID, '-') AS KeycardID,
                        COALESCE(Customer_TBL.FirstName || ' ' || Customer_TBL.LastName, '-') AS CustomerName,
                        COALESCE(Apartment_Info_TBL.RoomNo, '-') AS RoomNo,
                        COALESCE(Employee_TBL.FirstName || ' ' || Employee_TBL.LastName, '-') AS EmployeeName,
                        CASE 
                            WHEN Access_Card_Manage_TBL.Status = 'Idle' THEN 'ว่าง'
                            WHEN Access_Card_Manage_TBL.Status = 'Used' THEN 'ใช้งานอยู่'
                            ELSE '-'
                        END AS Status  
                    FROM Access_Card_Manage_TBL
                    LEFT JOIN Customer_TBL ON Access_Card_Manage_TBL.CustomerID = Customer_TBL.CustomerID
                    LEFT JOIN Contract_TBL ON Customer_TBL.CustomerID = Contract_TBL.CustomerID
                    LEFT JOIN Apartment_Info_TBL ON Contract_TBL.RoomID = Apartment_Info_TBL.RoomID
                    LEFT JOIN Employee_TBL ON Access_Card_Manage_TBL.StaffID = Employee_TBL.EmployeeID
                    ORDER BY Access_Card_Manage_TBL.ID;
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
        self.display_show_all_keycard()

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        for index, item in enumerate(data):
            self.tree.move(item[1], '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def on_close(self):
        self.master.deiconify()  # Show the main page
        self.destroy()