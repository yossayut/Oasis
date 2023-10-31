import tkinter as tk
import sqlite3

from tkinter                        import messagebox, ttk
from GetData.GetEmployeeName        import get_employee_name
from GetData.GetCurrentCustomerName import get_current_customer_name
from Config.Config                  import *


class KeycardPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x500")
        self.title("คีย์การ์ด")

        ##########################################################################################
        #   Key Card no.                                                                         #
        ##########################################################################################
        keycard_frame = ttk.LabelFrame(self, text="คีย์การ์ด", padding=10)
        keycard_frame.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        label_instruction = tk.Label(keycard_frame, text="แสกนคีย์การ์ด")
        label_instruction.grid(row=0, column=0, pady=10)
        self.entry_text   = tk.Entry(keycard_frame)
        self.entry_text.focus()
        self.entry_text.grid(row=0, column=1, pady=10)
        
        ##########################################################################################
        #   Withdraw / Deposite                                                                  #
        ##########################################################################################
        transaction_frame = ttk.LabelFrame(self, text="รายการ", padding=10)
        transaction_frame.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        self.transaction_type      = tk.StringVar(value="withdraw")
        transaction_radio_withdraw = ttk.Radiobutton(transaction_frame, text="เบิก", variable=self.transaction_type, value="withdraw")
        transaction_radio_withdraw.grid(row=0, column=0)
        transaction_radio_deposite = ttk.Radiobutton(transaction_frame, text="คืน", variable=self.transaction_type, value="deposite")
        transaction_radio_deposite.grid(row=0, column=1)

        ##########################################################################################
        #   Customer / Employee                                                                  #
        ##########################################################################################
        user_frame = ttk.LabelFrame(self, text="ผู้ทำรายการ", padding=10)
        user_frame.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        self.customer_employee = tk.StringVar(value="customer")
        customer_radio         = ttk.Radiobutton(user_frame, text="ลูกค้า", variable=self.customer_employee, value="customer")
        customer_radio.grid(row=0, column=0)

        self.customer_names    = get_current_customer_name()  # Customer names

        self.selected_customer = tk.StringVar()
        self.selected_customer.set("*เลือกลูกค้า") 
        self.customer_dropdown = tk.OptionMenu(user_frame, self.selected_customer, *self.customer_names)
        self.customer_dropdown.grid(row=0, column=1, pady=10)

        ##########################################################################################

        employee_radio         = ttk.Radiobutton(user_frame, text="พนักงาน", variable=self.customer_employee, value="employee")
        employee_radio.grid(row=0, column=3)

        self.employee_names    = get_employee_name()  # employee names

        self.selected_employee = tk.StringVar()
        self.selected_employee.set("*เลือกพนักงาน") 
        self.employee_dropdown = tk.OptionMenu(user_frame, self.selected_employee, *self.employee_names)
        self.employee_dropdown.grid(row=0, column=4, pady=10)


        ##########################################################################################
        #   employee Filler                                                                         #
        ##########################################################################################
        filler_frame = ttk.LabelFrame(self, text="ผู้กรอก", padding=10)
        filler_frame.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        self.selected_filler = tk.StringVar()
        self.selected_filler.set("*เลือกพนักงาน") 
        self.filler_dropdown = tk.OptionMenu(filler_frame, self.selected_filler, *self.employee_names)
        self.filler_dropdown.grid(row=1, column=1, pady=10)

        ##########################################################################################
        ok_button = tk.Button(self, text="OK", command=self.record_data)
        ok_button.grid(row=7, column=1, columnspan=2, pady=20)

        self.columnconfigure(1, weight=1)

    def record_data(self):

        card_number             = self.entry_text.get()  # Get the input text
        customer_transaction    = self.selected_customer.get()
        employee_transaction    = self.selected_employee.get()

        
        employee_filler         = self.selected_filler.get()

        transaction_radio       = self.transaction_type.get()
        customer_employee_radio = self.customer_employee.get()


        if DEBUG == True :
            print(card_number)
            print(customer_transaction)
            print(employee_transaction)
            print(employee_filler)

            print(transaction_radio)
            print(customer_employee_radio)

        conn = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            if self.transaction_type.get() == "withdraw" and self.customer_employee.get() == "employee" :
                print("พนักงานเบิก access card")

                cursor.execute("""
                    UPDATE Access_Card_Manage_TBL
                    SET Status = "Used", StaffID = ?
                    WHERE KeycardID = ?
                """, (employee_transaction, card_number))

                conn.commit()
                conn.close()

            elif self.transaction_type.get() == "withdraw" and self.customer_employee.get() == "customer" :  
                print("ลูกค้าเบิก access card")         

            elif self.transaction_type.get() == "deposite" and self.customer_employee.get() == "employee" :
                print("พนักงานคืน access card")  

            elif self.transaction_type.get() == "deposite" and self.customer_employee.get() == "customer" : 
                print("ลูกค้าคืน access card")  

            else :
                print("no")


        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()
