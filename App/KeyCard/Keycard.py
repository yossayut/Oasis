import tkinter as tk
import sqlite3

from tkinter                        import messagebox, ttk
from GetData.GetEmployeeName        import get_employee_name_from_DB
from GetData.GetEmployeeID          import get_employee_id_from_first_last_name
from GetData.GetCustomerID          import get_customer_id_from_first_last_name
from GetData.GetCurrentCustomerName import get_current_customer_name_from_DB
from Config.Config                  import *
from KeyCard.KeycardCheck           import keycard_check

global txt_staff_fill 

txt_staff_fill = "พนักงานกรอก"

class KeycardPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("400x500")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind('<Escape>', self.on_escape)
        self.title("คีย์การ์ด")

        txt_keycard              = "คีย์การ์ด"
        txt_scan_keycard         = "แสกนหรือพิมพ์เลขคีย์การ์ด"
        txt_transaction          = "รายการ"
        txt_transaction_withdraw = "เบิก"
        txt_transaction_deposite = "คืน"
        txt_transaction_lost     = "หาย"
        txt_transaction_who      = "ผู้ทำรายการ"
        txt_transaction_customer = "ลูกค้า"
        txt_transaction_staff    = "พนักงาน"

        ##########################################################################################
        #   Key Card no.                                                                         #
        ##########################################################################################
        keycard_frame = ttk.LabelFrame(self, text=txt_keycard, padding=10)
        keycard_frame.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        label_instruction = tk.Label(keycard_frame, text=txt_scan_keycard)
        label_instruction.grid(row=0, column=0, pady=10)

        self.entry_text   = tk.Entry(keycard_frame)
        self.entry_text.focus()
        self.entry_text.grid(row=0, column=1, pady=10)
        
        ##########################################################################################
        #   Withdraw / Deposite                                                                  #
        ##########################################################################################
        transaction_frame = ttk.LabelFrame(self, text=txt_transaction, padding=10)
        transaction_frame.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        self.transaction_type      = tk.StringVar(value="withdraw")

        transaction_radio_withdraw = ttk.Radiobutton(transaction_frame, text=txt_transaction_withdraw, variable=self.transaction_type, value="withdraw")
        transaction_radio_withdraw.grid(row=0, column=0)

        transaction_radio_deposite = ttk.Radiobutton(transaction_frame, text=txt_transaction_deposite, variable=self.transaction_type, value="deposite")
        transaction_radio_deposite.grid(row=0, column=1)

        transaction_radio_deposite = ttk.Radiobutton(transaction_frame, text=txt_transaction_lost, variable=self.transaction_type, value="lost")
        transaction_radio_deposite.grid(row=0, column=2)

        ##########################################################################################
        #   Customer / Employee                                                                  #
        ##########################################################################################
        user_frame = ttk.LabelFrame(self, text=txt_transaction_who, padding=10)
        user_frame.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        self.customer_employee = tk.StringVar(value="customer")
        customer_radio         = ttk.Radiobutton(user_frame, text=txt_transaction_customer, variable=self.customer_employee, value="customer")
        customer_radio.grid(row=0, column=0)
        ###################################################################################
        self.customer_names    = get_current_customer_name_from_DB()  # Customer names
        ###################################################################################
        self.selected_customer = tk.StringVar()
        self.selected_customer.set("*เลือก" + txt_transaction_customer) 
        self.customer_dropdown = tk.OptionMenu(user_frame, self.selected_customer, *self.customer_names)
        self.customer_dropdown.grid(row=0, column=1, pady=10)

        employee_radio         = ttk.Radiobutton(user_frame, text=txt_transaction_staff, variable=self.customer_employee, value="employee")
        employee_radio.grid(row=0, column=3)
        ###################################################################################
        self.employee_names    = get_employee_name_from_DB()  # employee names
        ###################################################################################
        self.selected_employee = tk.StringVar()
        self.selected_employee.set("*เลือก" + txt_transaction_staff) 
        self.employee_dropdown = tk.OptionMenu(user_frame, self.selected_employee, *self.employee_names)
        self.employee_dropdown.grid(row=0, column=4, pady=10)

        ##########################################################################################
        #   employee Filler                                                                         #
        ##########################################################################################
        filler_frame = ttk.LabelFrame(self, text=txt_staff_fill, padding=10)
        filler_frame.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        self.selected_filler = tk.StringVar()
        self.selected_filler.set("*เลือก" + txt_staff_fill) 
        self.filler_dropdown = tk.OptionMenu(filler_frame, self.selected_filler, *self.employee_names)
        self.filler_dropdown.grid(row=1, column=1, pady=10)

        ##########################################################################################
        ok_button = tk.Button(self, text="OK", command=self.record_data)
        ok_button.grid(row=7, column=1, columnspan=2, pady=20)

        self.columnconfigure(1, weight=1)

    def record_data(self):
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            card_number             = self.entry_text.get()  # Get the input text
            card_number_exist_flag  = keycard_check(card_number)
            transaction_radio       = self.transaction_type.get()
            employee_filler         = self.selected_filler.get()

            ##########################################################################################
            #   employee Withdraw                                                                    #
            ##########################################################################################

            # card number is OK
            if card_number_exist_flag == True :

                # staff name is filled
                if employee_filler != "*เลือก" + txt_staff_fill :

                    if self.transaction_type.get() == "withdraw" and self.customer_employee.get() == "employee" :
                        if DEBUG == True : 
                            print("พนักงานเบิก access card")  

                        customer_employee_radio     = self.customer_employee.get()
                        employee_name               = self.selected_employee.get()
                        employee_name_parts         = employee_name.strip("()").replace("'", "").split(", ")
                        employee_id                 = get_employee_id_from_first_last_name(employee_name_parts[0],employee_name_parts[1])

                        employee_filler_name_parts  = employee_filler.strip("()").replace("'", "").split(", ")
                        employee_filler_id          = get_employee_id_from_first_last_name(employee_filler_name_parts[0],employee_filler_name_parts[1])

                        cursor.execute("""
                                            UPDATE Access_Card_Manage_TBL
                                            SET Status = "Used", StaffID = ?
                                            WHERE KeycardID = ?
                                       """, (employee_id, card_number))

                        conn.commit()
                        conn.close()

                        self.after_transaction(card_number, employee_name, "พนักงานเบิกบัตร")

                    ##########################################################################################
                    #   customer Withdraw                                                                    #
                    ##########################################################################################
                    elif self.transaction_type.get() == "withdraw" and self.customer_employee.get() == "customer" :  
                        if DEBUG == True : 
                            print("ลูกค้าเบิก access card")  

                        customer_employee_radio     = self.customer_employee.get()
                        customer_name               = self.selected_customer.get()
                        customer_name_parts         = customer_name.strip("()").replace("'", "").split(", ")
                        customer_id                 = get_customer_id_from_first_last_name(customer_name_parts[0],customer_name_parts[1])

                        employee_filler_name_parts  = employee_filler.strip("()").replace("'", "").split(", ")
                        employee_filler_id          = get_employee_id_from_first_last_name(employee_filler_name_parts[0],employee_filler_name_parts[1])

                        cursor.execute("""
                                            UPDATE Access_Card_Manage_TBL
                                            SET Status = "Used", CustomerID = ?, StaffID = ?
                                            WHERE KeycardID = ?
                                       """, (customer_id, employee_filler_id, card_number))

                        conn.commit()
                        conn.close()

                        self.after_transaction(card_number, customer_name, "ลูกค้าเบิกบัตร")

                    ##########################################################################################
                    #   employee or customer deposite                                                        #
                    ##########################################################################################
                    elif self.transaction_type.get() == "deposite" :
                        if DEBUG == True : 
                            print("คืน access card")  

                        cursor.execute("""
                                            UPDATE Access_Card_Manage_TBL
                                            SET Status = "Idle", CustomerID = NULL, StaffID = NULL
                                            WHERE KeycardID = ?
                                       """, (card_number,))

                        conn.commit()
                        conn.close()
                   
                        self.after_transaction(card_number, "N/A", "คืนบัตร")

                    ##########################################################################################
                    #   employee or customer lost                                                        #
                    ##########################################################################################
                    elif self.transaction_type.get() == "lost" :
                        if DEBUG == True : 
                            print("access card หาย")  

                        cursor.execute("""
                                            UPDATE Access_Card_Manage_TBL
                                            SET Status = "Lost"
                                            WHERE KeycardID = ?
                                       """, (card_number,))

                        conn.commit()
                        conn.close()
                   
                        self.after_transaction(card_number, "N/A", "หาย")

                    else :
                        print("no")
                
                else :
                    messagebox.showinfo("Warning", "กรุณาเลือกพนักงานกรอกข้อมูล")         
            else :
                messagebox.showinfo("Warning", "กรุณาใส่ข้อมูลบัตรที่ถูกต้อง")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()

    def after_transaction(self, card_number, staff_name, transaction_type):
        message = f"Transaction Successful!\nCard Number: {card_number}\nStaff Name: {staff_name}\nTransaction Type: {transaction_type}"
        messagebox.showinfo("Transaction Info", message)
        self.destroy()           # Closes the current window
        self.master.deiconify()  # Show the main page

    def on_close(self):
        self.master.deiconify()  # Show the main page
        self.destroy()

    def on_escape(self, event):
        self.on_close()                                # Close the current window