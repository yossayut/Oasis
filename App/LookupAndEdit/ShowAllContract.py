import tkinter as tk
import sqlite3

from tkinter         import ttk
from Config.Config   import *

class Show_all_contract_Page(tk.Toplevel):
    def change_filter(self, option):
        self.filter_var.set(option)
        self.apply_filter()

    def __init__(self, master):
        super().__init__(master)
        self.title("สัญญาทั้งหมด")
        self.geometry("1200x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()
        self.bind('<Escape>', self.on_escape)

    def create_widgets(self):
        paned_window = ttk.Panedwindow(self, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        filter_frame = ttk.Frame(paned_window)
        paned_window.add(filter_frame)

        self.filter_var = tk.StringVar(value="สัญญาทั้งหมด")

        tk.Label(filter_frame, text="สัญญาทั้งหมด : ").grid(row=0, column=0)                          

        ttk.Radiobutton(filter_frame, 
            text="เรียงตามลำดับที่", 
            value="Show_all_order_by_no", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_all_order_by_no")).grid(row=0, column=1, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="เรียงตามเบอร์ห้อง", 
            value="Show_all_order_by_room", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_all_order_by_room")).grid(row=0, column=2, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="เรียงตามลูกค้า", 
            value="Show_all_order_by_customer", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_all_order_by_customer")).grid(row=0, column=3, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="เรียงตามวันเริ่มสัญญา", 
            value="Show_all_order_by_start_date", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_all_order_by_start_date")).grid(row=0, column=4, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="เรียงตามวันสิ้นสุดสัญญา", 
            value="Show_all_order_by_end_date", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_all_order_by_end_date")).grid(row=0, column=5, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="เรียงตามพนักงาน", 
            value="Show_all_order_by_staff", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show_all_order_by_staff")).grid(row=0, column=6, padx=10)

#############################################################################################################
        # ttk.Radiobutton(filter_frame, 
        #     text="เฉพาะห้องที่มีสัญญา", 
        #     value="Contrat_Active", 
        #     variable=self.filter_var, 
        #     command=lambda: self.change_filter("Contrat_Active")).grid(row=0, column=1, padx=10)

        # ttk.Radiobutton(filter_frame, 
        #     text="เฉพาะสัญญาหมดอายุ", 
        #     value="Contract_Expired", 
        #     variable=self.filter_var, 
        #     command=lambda: self.change_filter("Contract_Expired")).grid(row=0, column=2, padx=10)

        # ttk.Radiobutton(filter_frame, 
        # 	text="เฉพาะยกเลิกสัญญา", 
        # 	value="Contract_Quit", 
        # 	variable=self.filter_var, 
        # 	command=lambda: self.change_filter("Contract_Quit")).grid(row=0, column=3, padx=10)

        self.tree = ttk.Treeview(paned_window,  
             columns=("ContractID", "RoomID", "CustomerID", "StartDate", "EndDate", 
                "StaffID", "RoomFee","MaintenanceFee","ParkingFee","Remark","Status"), 
        	show="headings")

        txt_number      = "ลำดับที่"
        txt_room_no     = "เบอร์ห้อง"
        txt_customer    = "ลูกค้า"
        txt_start       = "เริ่มต้น"
        txt_end         = "สิ้นสุด"
        txt_staff       = "พนักงาน"
        txt_room_fee    = "ค่าเช่าห้อง"
        txt_common_fee  = "ค่าส่วนกลาง"
        txt_parking_fee = "ค่าจอดรถ"
        txt_etc         = "อื่นๆ"
        txt_status      = "สถานะ"

        self.tree.heading("#1", text=txt_number      , command=lambda: self.sort_treeview(1, True))
        self.tree.heading("#2", text=txt_room_no     , command=lambda: self.sort_treeview(2, True))
        self.tree.heading("#3", text=txt_customer    , command=lambda: self.sort_treeview(3, True))
        self.tree.heading("#4", text=txt_start       , command=lambda: self.sort_treeview(4, True))
        self.tree.heading("#5", text=txt_end         , command=lambda: self.sort_treeview(5, True))
        self.tree.heading("#6", text=txt_staff       , command=lambda: self.sort_treeview(6, True))
        self.tree.heading("#7", text=txt_room_fee    , command=lambda: self.sort_treeview(7, True))
        self.tree.heading("#8", text=txt_common_fee  , command=lambda: self.sort_treeview(8, True))
        self.tree.heading("#9", text=txt_parking_fee , command=lambda: self.sort_treeview(9, True))
        self.tree.heading("#10", text=txt_etc        , command=lambda: self.sort_treeview(10, True))
        self.tree.heading("#11", text=txt_status     , command=lambda: self.sort_treeview(11, True))

        self.tree.column("#1",  width=40,   anchor="center")
        self.tree.column("#2",  width=80,   anchor="center")
        self.tree.column("#3",  width=100,  anchor="center")
        self.tree.column("#4",  width=80,   anchor="center")
        self.tree.column("#5",  width=80,   anchor="center")
        self.tree.column("#6",  width=80,   anchor="center")
        self.tree.column("#7",  width=80,   anchor="center")
        self.tree.column("#8",  width=80,   anchor="center")
        self.tree.column("#9",  width=80,   anchor="center")
        self.tree.column("#10", width=80,   anchor="center")
        self.tree.column("#11", width=80,   anchor="center")

        paned_window.add(self.tree)
        self.display_show_all_contract()

    def display_show_all_contract(self):
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            if self.filter_var.get() == "Show_all_order_by_no" :
                if DEBUG == True :
                    print("1.เรียงตามลำดับที่")
                # Show all rooms
                cursor.execute("""
                    SELECT 
                        Contract_TBL.ContractID, 
                        Apartment_Info_TBL.RoomNo, 
                        Customer_TBL.FirstName || ' ' || Customer_TBL.LastName || "(" || Customer_TBL.NickName || ")" AS CustomerName,  -- Add "AS CustomerName"
                        Contract_TBL.StartDate,
                        Contract_TBL.EndDate,
                        Employee_TBL.FirstName || ' ' || Employee_TBL.LastName AS EmployeeName,  -- Add "AS EmployeeName"
                        Contract_TBL.RoomFee,
                        Contract_TBL.MaintenanceFee,
                        Contract_TBL.ParkingFee,
                        Contract_TBL.Remark,
                        Contract_TBL.Status
                    FROM Contract_TBL
                    INNER JOIN Apartment_Info_TBL ON Contract_TBL.RoomID     = Apartment_Info_TBL.RoomID
                    INNER JOIN Customer_TBL       ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    INNER JOIN Employee_TBL       ON Contract_TBL.StaffID    = Employee_TBL.EmployeeID
                    ORDER BY Contract_TBL.ContractID ;
                """)

            elif self.filter_var.get() == "Show_all_order_by_room" :
                if DEBUG == True :
                    print("2.เรียงตามเบอร์ห้อง")

                # Show all rooms
                cursor.execute("""
                    SELECT 
                        Contract_TBL.ContractID, 
                        Apartment_Info_TBL.RoomNo, 
                        Customer_TBL.FirstName || ' ' || Customer_TBL.LastName || "(" || Customer_TBL.NickName || ")" AS CustomerName,  -- Add "AS CustomerName"
                        Contract_TBL.StartDate,
                        Contract_TBL.EndDate,
                        Employee_TBL.FirstName || ' ' || Employee_TBL.LastName AS EmployeeName,  -- Add "AS EmployeeName"
                        Contract_TBL.RoomFee,
                        Contract_TBL.MaintenanceFee,
                        Contract_TBL.ParkingFee,
                        Contract_TBL.Remark,
                        Contract_TBL.Status
                    FROM Contract_TBL
                    INNER JOIN Apartment_Info_TBL ON Contract_TBL.RoomID     = Apartment_Info_TBL.RoomID
                    INNER JOIN Customer_TBL       ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    INNER JOIN Employee_TBL       ON Contract_TBL.StaffID    = Employee_TBL.EmployeeID
                    ORDER BY Apartment_Info_TBL.RoomNo ;
                """)

            elif self.filter_var.get() == "Show_all_order_by_customer" :
                if DEBUG == True :
                    print("3.เรียงตามลูกค้า")                
                # Show all rooms
                cursor.execute("""
                    SELECT 
                        Contract_TBL.ContractID, 
                        Apartment_Info_TBL.RoomNo, 
                        Customer_TBL.FirstName || ' ' || Customer_TBL.LastName || "(" || Customer_TBL.NickName || ")" AS CustomerName,  -- Add "AS CustomerName"
                        Contract_TBL.StartDate,
                        Contract_TBL.EndDate,
                        Employee_TBL.FirstName || ' ' || Employee_TBL.LastName AS EmployeeName,  -- Add "AS EmployeeName"
                        Contract_TBL.RoomFee,
                        Contract_TBL.MaintenanceFee,
                        Contract_TBL.ParkingFee,
                        Contract_TBL.Remark,
                        Contract_TBL.Status
                    FROM Contract_TBL
                    INNER JOIN Apartment_Info_TBL ON Contract_TBL.RoomID     = Apartment_Info_TBL.RoomID
                    INNER JOIN Customer_TBL       ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    INNER JOIN Employee_TBL       ON Contract_TBL.StaffID    = Employee_TBL.EmployeeID
                    ORDER BY Customer_TBL.FirstName ;
                """)

            elif self.filter_var.get() == "Show_all_order_by_start_date" :
                if DEBUG == True :
                    print("4.เรียงตามวันเริ่มสัญญา")                  
                # Show all rooms
                cursor.execute("""
                    SELECT 
                        Contract_TBL.ContractID, 
                        Apartment_Info_TBL.RoomNo, 
                        Customer_TBL.FirstName || ' ' || Customer_TBL.LastName || "(" || Customer_TBL.NickName || ")" AS CustomerName,  -- Add "AS CustomerName"
                        Contract_TBL.StartDate,
                        Contract_TBL.EndDate,
                        Employee_TBL.FirstName || ' ' || Employee_TBL.LastName AS EmployeeName,  -- Add "AS EmployeeName"
                        Contract_TBL.RoomFee,
                        Contract_TBL.MaintenanceFee,
                        Contract_TBL.ParkingFee,
                        Contract_TBL.Remark,
                        Contract_TBL.Status
                    FROM Contract_TBL
                    INNER JOIN Apartment_Info_TBL ON Contract_TBL.RoomID     = Apartment_Info_TBL.RoomID
                    INNER JOIN Customer_TBL       ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    INNER JOIN Employee_TBL       ON Contract_TBL.StaffID    = Employee_TBL.EmployeeID
                    ORDER BY Contract_TBL.StartDate ;
                """)

            elif self.filter_var.get() == "Show_all_order_by_end_date" :
                if DEBUG == True :
                    print("5.เรียงตามวันสิ้นสุดสัญญา")                  
                # Show all rooms
                cursor.execute("""
                    SELECT 
                        Contract_TBL.ContractID, 
                        Apartment_Info_TBL.RoomNo, 
                        Customer_TBL.FirstName || ' ' || Customer_TBL.LastName || "(" || Customer_TBL.NickName || ")" AS CustomerName,  -- Add "AS CustomerName"
                        Contract_TBL.StartDate,
                        Contract_TBL.EndDate,
                        Employee_TBL.FirstName || ' ' || Employee_TBL.LastName AS EmployeeName,  -- Add "AS EmployeeName"
                        Contract_TBL.RoomFee,
                        Contract_TBL.MaintenanceFee,
                        Contract_TBL.ParkingFee,
                        Contract_TBL.Remark,
                        Contract_TBL.Status
                    FROM Contract_TBL
                    INNER JOIN Apartment_Info_TBL ON Contract_TBL.RoomID     = Apartment_Info_TBL.RoomID
                    INNER JOIN Customer_TBL       ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    INNER JOIN Employee_TBL       ON Contract_TBL.StaffID    = Employee_TBL.EmployeeID
                    ORDER BY Contract_TBL.EndDate ;
                """)

            elif self.filter_var.get() == "Show_all_order_by_staff" :
                if DEBUG == True :
                    print("6.เรียงตามพนักงาน")                   
                # Show all rooms
                cursor.execute("""
                    SELECT 
                        Contract_TBL.ContractID, 
                        Apartment_Info_TBL.RoomNo, 
                        Customer_TBL.FirstName || ' ' || Customer_TBL.LastName || "(" || Customer_TBL.NickName || ")" AS CustomerName,  -- Add "AS CustomerName" 
                        Contract_TBL.StartDate,
                        Contract_TBL.EndDate,
                        Employee_TBL.FirstName || ' ' || Employee_TBL.LastName AS EmployeeName,  -- Add "AS EmployeeName"
                        Contract_TBL.RoomFee,
                        Contract_TBL.MaintenanceFee,
                        Contract_TBL.ParkingFee,
                        Contract_TBL.Remark,
                        Contract_TBL.Status
                    FROM Contract_TBL
                    INNER JOIN Apartment_Info_TBL ON Contract_TBL.RoomID     = Apartment_Info_TBL.RoomID
                    INNER JOIN Customer_TBL       ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    INNER JOIN Employee_TBL       ON Contract_TBL.StaffID    = Employee_TBL.EmployeeID
                    ORDER BY Employee_TBL.FirstName ;
                """)

            else :
                if DEBUG == True :
                    print("7.เรียงตามลำดับที่")  

                cursor.execute("""
                    SELECT 
                        Contract_TBL.ContractID, 
                        Apartment_Info_TBL.RoomNo, 
                        Customer_TBL.FirstName || ' ' || Customer_TBL.LastName || "(" || Customer_TBL.NickName || ")" AS CustomerName,  -- Add "AS CustomerName"
                        Contract_TBL.StartDate,
                        Contract_TBL.EndDate,
                        Employee_TBL.FirstName || ' ' || Employee_TBL.LastName AS EmployeeName,  -- Add "AS EmployeeName"
                        Contract_TBL.RoomFee,
                        Contract_TBL.MaintenanceFee,
                        Contract_TBL.ParkingFee,
                        Contract_TBL.Remark,
                        Contract_TBL.Status
                    FROM Contract_TBL
                    INNER JOIN Apartment_Info_TBL ON Contract_TBL.RoomID     = Apartment_Info_TBL.RoomID
                    INNER JOIN Customer_TBL       ON Contract_TBL.CustomerID = Customer_TBL.CustomerID
                    INNER JOIN Employee_TBL       ON Contract_TBL.StaffID    = Employee_TBL.EmployeeID
                    ORDER BY Contract_TBL.ContractID ;
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
        self.display_show_all_contract()

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        for index, item in enumerate(data):
            self.tree.move(item[1], '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def on_close(self):
        self.master.deiconify()  # Show the main page
        self.destroy()

    def on_escape(self, event):
        self.on_close()                                # Close the current window