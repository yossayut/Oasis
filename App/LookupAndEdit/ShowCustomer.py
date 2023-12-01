import tkinter as tk
import sqlite3

from tkinter         import ttk
from Config.Config   import *

class Show_customer_Page(tk.Toplevel):
    def change_filter(self, option):
        self.filter_var.set(option)
        self.apply_filter()

    def __init__(self, master):
        super().__init__(master)
        self.title("ลูกค้าทั้งหมด")
        self.geometry("1600x600")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.create_widgets()
        self.bind('<Escape>', self.on_escape)
        
    def create_widgets(self):
        paned_window = ttk.Panedwindow(self, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        filter_frame = ttk.Frame(paned_window)
        paned_window.add(filter_frame)

        self.filter_var = tk.StringVar(value="ลูกค้าทั้งหมด")

        ttk.Radiobutton(filter_frame, 
            text="ลูกค้าทั้งหมด", 
            value="Show all", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Show all")).grid(row=0, column=0, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="ลูกค้าเก่า", 
            value="Expired customer", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Expired customer")).grid(row=0, column=1, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="ลูกค้าปัจจุบัน", 
            value="Active customer", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("Active customer")).grid(row=0, column=2, padx=10)

        ttk.Radiobutton(filter_frame, 
            text="ลูกค้าทั้งหมดเรียงตามชื่อ", 
            value="All customer order by name", 
            variable=self.filter_var, 
            command=lambda: self.change_filter("All customer order by name")).grid(row=0, column=3, padx=10)

        self.tree = ttk.Treeview(paned_window, 
        	columns=("customerID","Prefix","FirstName","LastName","NickName","ThaiNationalID","BirthDay","AddressNumber","AddressCont","AddressRoad","AddressSubProvince","AddressProvince","AddressCity","Phone","LineID","Job","ReferencePerson","RegisterDate"), 
        	show="headings")

        txt_customerID                  = "ลำดับที่"
        txt_prefix                      = "คำนำหน้าชื่อ"
        txt_customer_first_name         = "ชื่อ"
        txt_customer_last_name          = "นามสกุล"
        txt_customer_nick_name          = "ชื่อเล่น"
        txt_customer_id                 = "เลขบัตรประชาชน"
        txt_customer_birth_day          = "วัน/เดือน/ปี เกิด"

        txt_address                     = "ที่อยู่เลขที่"
        txt_address_cont                = "ที่อยู่(ต่อ)"
        txt_road                        = "ถนน"
        txt_sub_province                = "แขวง/ตำบล"
        txt_province                    = "เขต/อำเภอ"
        txt_city                        = "จังหวัด"
        txt_tel_no                      = "เบอร์โทร"
        txt_lineid                      = "LineID"
        txt_job                         = "อาชีพ"
        txt_emergency_contact           = "ติดต่อฉุกเฉิน"
        txt_start_customer              = "วันที่เริ่มต้น"

        self.tree.heading("#1",  text=txt_customerID           ,  command=lambda: self.sort_treeview(1, True))
        self.tree.heading("#2",  text=txt_prefix               ,  command=lambda: self.sort_treeview(2, True))
        self.tree.heading("#3",  text=txt_customer_first_name  ,  command=lambda: self.sort_treeview(3, True))
        self.tree.heading("#4",  text=txt_customer_last_name   ,  command=lambda: self.sort_treeview(4, True))
        self.tree.heading("#5",  text=txt_customer_nick_name   ,  command=lambda: self.sort_treeview(5, True))
        self.tree.heading("#6",  text=txt_customer_id          ,  command=lambda: self.sort_treeview(6, True))
        self.tree.heading("#7",  text=txt_customer_birth_day   ,  command=lambda: self.sort_treeview(7, True))

        self.tree.heading("#8",  text=txt_address              ,  command=lambda: self.sort_treeview(8, True))
        self.tree.heading("#9",  text=txt_address_cont         ,  command=lambda: self.sort_treeview(9, True))
        self.tree.heading("#10", text=txt_road                 ,  command=lambda: self.sort_treeview(10, True))
        self.tree.heading("#11", text=txt_sub_province         ,  command=lambda: self.sort_treeview(11, True))
        self.tree.heading("#12", text=txt_province             ,  command=lambda: self.sort_treeview(12, True))
        self.tree.heading("#13", text=txt_city                 ,  command=lambda: self.sort_treeview(13, True))
        self.tree.heading("#14", text=txt_tel_no               ,  command=lambda: self.sort_treeview(14, True))
        self.tree.heading("#15", text=txt_lineid               ,  command=lambda: self.sort_treeview(15, True))
        self.tree.heading("#16", text=txt_job                  ,  command=lambda: self.sort_treeview(16, True))
        self.tree.heading("#17", text=txt_emergency_contact    ,  command=lambda: self.sort_treeview(17, True))
        self.tree.heading("#18", text=txt_start_customer       ,  command=lambda: self.sort_treeview(18, True))
      

        self.tree.column("#1",  width=40,   anchor="center")
        self.tree.column("#2",  width=80,   anchor="center")
        self.tree.column("#3",  width=80,   anchor="center")
        self.tree.column("#4",  width=80,   anchor="center")
        self.tree.column("#5",  width=80,   anchor="center")
        self.tree.column("#6",  width=120,  anchor="center")
        self.tree.column("#7",  width=80,   anchor="center")
        self.tree.column("#8",  width=80,   anchor="center")
        self.tree.column("#9",  width=80,   anchor="center")
        self.tree.column("#10", width=80,   anchor="center")
        self.tree.column("#11", width=80,   anchor="center")
        self.tree.column("#12", width=80,   anchor="center")
        self.tree.column("#13", width=80,   anchor="center")
        self.tree.column("#14", width=80,   anchor="center")
        self.tree.column("#15", width=80,   anchor="center")
        self.tree.column("#16", width=80,   anchor="center")
        self.tree.column("#17", width=80,   anchor="center")
        self.tree.column("#18", width=80,   anchor="center")

        paned_window.add(self.tree)
        self.display_show_all_customer()

    def display_show_all_customer(self):
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            if self.filter_var.get() == "Show all":
                if DEBUG == True :
                    print("1.ลูกค้าทั้งหมดเรียงตามชื่อ")

                cursor.execute("""
                    SELECT * 
                    FROM Customer_TBL
                    ORDER BY Customer_TBL.FirstName;
                """)

            elif self.filter_var.get() == "Expired customer":
                if DEBUG == True :
                    print("2.ลูกค้าเก่า")

                cursor.execute("""
                    SELECT DISTINCT
                        Customer_TBL.CustomerID,
                        Customer_TBL.Prefix,
                        Customer_TBL.FirstName,
                        Customer_TBL.LastName,
                        Customer_TBL.NickName,
                        Customer_TBL.ThaiNationalID,
                        Customer_TBL.BirthDay,
                        Customer_TBL.AddressNumber,
                        Customer_TBL.AddressCont,
                        Customer_TBL.AddressRoad,
                        Customer_TBL.AddressSubProvince,
                        Customer_TBL.AddressProvince,
                        Customer_TBL.AddressCity,
                        Customer_TBL.Phone,
                        Customer_TBL.LineID,
                        Customer_TBL.Job,
                        Customer_TBL.ReferencePerson,
                        Customer_TBL.RegisterDate
                    FROM
                        Customer_TBL
                    WHERE
                        NOT EXISTS (
                            SELECT 1
                            FROM Contract_TBL
                            WHERE
                                Contract_TBL.CustomerID = Customer_TBL.CustomerID
                                AND Contract_TBL.Status = 'Active'
                                AND (Contract_TBL.EndDate >= CURRENT_DATE OR Contract_TBL.EndDate IS NULL)
                        );
                """)

            elif self.filter_var.get() == "Active customer":
                if DEBUG == True :
                    print("3.ลูกค้าปัจจุบัน")

                cursor.execute("""
                    SELECT DISTINCT
                        Customer_TBL.CustomerID,
                        Customer_TBL.Prefix,
                        Customer_TBL.FirstName,
                        Customer_TBL.LastName,
                        Customer_TBL.NickName,
                        Customer_TBL.ThaiNationalID,
                        Customer_TBL.BirthDay,
                        Customer_TBL.AddressNumber,
                        Customer_TBL.AddressCont,
                        Customer_TBL.AddressRoad,
                        Customer_TBL.AddressSubProvince,
                        Customer_TBL.AddressProvince,
                        Customer_TBL.AddressCity,
                        Customer_TBL.Phone,
                        Customer_TBL.LineID,
                        Customer_TBL.Job,
                        Customer_TBL.ReferencePerson,
                        Customer_TBL.RegisterDate
                    FROM
                        Customer_TBL
                    JOIN Contract_TBL ON Customer_TBL.CustomerID = Contract_TBL.CustomerID
                    WHERE
                        Contract_TBL.Status = 'Active';
                """)

            else:
                if DEBUG == True :
                    print("4.ลูกค้าทั้งหมด")      

                cursor.execute("""
                    SELECT * 
                    FROM Customer_TBL
                    ORDER BY Customer_TBL.FirstName;
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
        self.display_show_all_customer()

    def sort_treeview(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        for index, item in enumerate(data):
            self.tree.move(item[1], '', index)
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

    def on_close(self):
        self.master.deiconify()                        # Show the main page
        self.destroy()

    def on_escape(self, event):
        self.on_close()                                # Close the current window