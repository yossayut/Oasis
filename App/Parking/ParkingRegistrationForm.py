import tkinter as tk
import sqlite3
import os

from tkinter  import messagebox, simpledialog
from datetime import datetime, timedelta

from Config.Config       import *

from Contract.CustomerExist                import CustomerExistPage
from Contract.FillCustomerDatabase         import fill_customer_database
from Contract.ContractFillPrepare          import prepare_contract_info, fill_contract_info
from Contract.GetCustomerInfoSubmitForm    import get_customer_info_submit_form
from GetData.GetEmployeeName               import get_employee_name

#############################################################################################################
# Create ParkingPage, It will show the available parking from Database and if select,
# it will go to the register form
#############################################################################################################
class ParkingRegistrationForm(tk.Toplevel):
    # 1 
    def __init__(self, master, room):
        super().__init__(master)
        self.title("ลงทะเบียนลูกค้าใหม่")
        self.geometry("600x500")
        self.room = room
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind('<Escape>', self.on_escape)
        # Establish the database connection

    # 2
    def create_widgets(self):
        ##########################################################################################
        #   Withdraw / Deposite                                                                  #
        ##########################################################################################
        type_frame = ttk.LabelFrame(self, text="ประเภท", padding=10)
        type_frame.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        self.automotive_type      = tk.StringVar(value="car")

        type_radio_car = ttk.Radiobutton(type_frame, text="รถยนต์", variable=self.automotive_type, value="car")
        type_radio_car.grid(row=0, column=0)

        type_radio_motocycle = ttk.Radiobutton(type_frame, text="มอเตอร์ไซต์", variable=self.automotive_type, value="motocycle")
        type_radio_motocycle.grid(row=0, column=1)

        ##########################################################################################
        #   Automotive detail                                                                    #
        ##########################################################################################
        detail_frame = ttk.LabelFrame(self, text="รายละเอียด", padding=10)
        detail_frame.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=10)

        label_brand_model = tk.Label(detail_frame, text="ยี่ห้อ/รุ่น")
        label_brand_model.grid(row=0, column=0, pady=10)
        self.entry_brand_model   = tk.Entry(detail_frame)
        self.entry_brand_model.focus()
        self.entry_brand_model.grid(row=0, column=1, pady=10)
        
        label_color = tk.Label(detail_frame, text="สี")
        label_color.grid(row=1, column=0, pady=10)
        self.entry_color   = tk.Entry(detail_frame)
        self.entry_color.focus()
        self.entry_color.grid(row=1, column=1, pady=10)       

        label_plate_no = tk.Label(detail_frame, text="สี")
        label_plate_no.grid(row=2, column=0, pady=10)
        self.entry_plate_no   = tk.Entry(detail_frame)
        self.entry_plate_no.focus()
        self.entry_plate_no.grid(row=2, column=1, pady=10)   

        ##########################################################################################
        ok_button = tk.Button(self, text="OK", command=self.record_data)
        ok_button.grid(row=7, column=1, columnspan=2, pady=20)

        self.columnconfigure(1, weight=1)

    # 4 : 
    def clear_form(self):
        self.prefix_entry.config(state=tk.NORMAL)
        self.first_name_entry.config(state=tk.NORMAL)
        self.last_name_entry.config(state=tk.NORMAL)
        self.nick_name_entry.config(state=tk.NORMAL)
        self.national_ID_entry.config(state=tk.NORMAL)


        # Clear other fields as needed
        self.prefix_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.nick_name_entry.delete(0, tk.END)
        self.national_ID_entry.delete(0, tk.END)

    def record_data(self):
        card_number             = self.entry_text.get()  # Get the input text
        transaction_radio       = self.transaction_type.get()

        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            ##########################################################################################
            #   employee Withdraw                                                                    #
            ##########################################################################################
            if self.transaction_type.get() == "withdraw" and self.customer_employee.get() == "employee" :
                print("พนักงานเบิก access card")  
                customer_employee_radio     = self.customer_employee.get()
                employee_name               = self.selected_employee.get()
                employee_name_parts         = employee_name.strip("()").replace("'", "").split(", ")
                employee_id                 = get_employee_id(employee_name_parts[0],employee_name_parts[1])

                employee_filler             = self.selected_filler.get()
                employee_filler_name_parts  = employee_filler.strip("()").replace("'", "").split(", ")
                employee_filler_id          = get_employee_id(employee_filler_name_parts[0],employee_filler_name_parts[1])

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
                print("ลูกค้าเบิก access card")  
                customer_employee_radio     = self.customer_employee.get()
                customer_name               = self.selected_customer.get()
                customer_name_parts         = customer_name.strip("()").replace("'", "").split(", ")
                customer_id                 = get_customer_id(customer_name_parts[0],customer_name_parts[1])

                employee_filler_name        = self.selected_filler.get()
                employee_filler_name_parts  = employee_filler_name.strip("()").replace("'", "").split(", ")
                employee_filler_id          = get_employee_id(employee_filler_name_parts[0],employee_filler_name_parts[1])

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
                print("คืน access card")  

                cursor.execute("""
                    UPDATE Access_Card_Manage_TBL
                    SET Status = "Idle", CustomerID = NULL, StaffID = NULL
                    WHERE KeycardID = ?
                """, (card_number,))

                conn.commit()
                conn.close()
           
                self.after_transaction(card_number, "N/A", "คืนบัตร")

            else :
                print("no")


        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()

    def after_transaction(self, card_number, staff_name, transaction_type):
        message = f"Transaction Successful!\nCard Number: {card_number}\nStaff Name: {staff_name}\nTransaction Type: {transaction_type}"
        messagebox.showinfo("Transaction Info", message)
        self.destroy()  # Closes the current window
        self.master.deiconify()  # Show the main page

    # 6
    def contract_submit_form(self):
        data = get_customer_info_submit_form(self) 
        if DEBUG == True :
            print(data)

        selected_room, prefix, first_name, last_name, nick_name, thai_national_id, birth_day, address_number, address_cont, \
        address_road, address_sub_province, address_province, address_city, phone, line_id, job, emergency, register_date,  \
        register_end_date, employee, room_fee, internet, maintenance, parking, remark = data
  
        if employee != "กรุณาเลือกพนักงาน":
            if first_name != "" or last_name != "" or thai_national_id != "" :

                ##################################################################################################################
                # Get contract information : ContractInformation.py
                # Prepare all information before fill contract database 
                # ex. 
                #     room information      from Apartment_Info_TBL
                #     customer information  from Customer_TBL
                #     employee name         from Employee_TBL
                ##################################################################################################################  
                inserted = fill_customer_database(prefix, first_name, last_name, nick_name, thai_national_id, birth_day, 
                    address_number, address_cont, address_road, address_sub_province, address_province, address_city, phone, 
                    line_id, job, emergency, register_date)
               
                if inserted:
                    self.clear_form()

                ##################################################################################################################
                # Get contract information : ContractInformation.py
                # Prepare all information before fill contract database 
                # ex. 
                #     room information      from Apartment_Info_TBL
                #     customer information  from Customer_TBL
                #     employee name         from Employee_TBL
                ##################################################################################################################         
                contract_info = prepare_contract_info(selected_room, first_name, last_name, register_date, register_end_date, employee,
                                                      remark)

                employee_names = employee.strip("()").split(", ")

                employee_first_name = employee_names[0].strip("'")  # Extract the first name
                employee_last_name = employee_names[1].strip("'")   # Extract the second name
                employee_name = employee_first_name + ' ' + employee_last_name

                if DEBUG == True :
                    print(employee_name)
                    print(contract_info)

                #########################################################
                # Fill contract to Database : ContractInformation.py
                # Fill Contract information to Contract_TBL
                #########################################################   
                RoomID_Input, RoomType_Input, CustomerID_Input, StartDate_Input, EndDate_Input, employeeID_Input, RoomFee_Input, \
                InternetFee_Input, MaintenanceFee_Input, ParkingFee_Input, Remark_Input, Status_Input = contract_info                 # Unpack contract info

                room_floor    = selected_room[1]
                room_building = selected_room[0]

                ##################################################################################################################
                # Get contract information : ContractInformation.py
                # Prepare all information before fill contract database 
                # ex. 
                #     room information      from Apartment_Info_TBL
                #     customer information  from Customer_TBL
                #     employee name         from Employee_TBL
                ################################################################################################################## 
                flag_fill_contract_info_success = fill_contract_info(RoomID_Input, CustomerID_Input, StartDate_Input, EndDate_Input, employeeID_Input, RoomFee_Input,
                                                                     InternetFee_Input, MaintenanceFee_Input, ParkingFee_Input, Remark_Input, Status_Input)

                if flag_fill_contract_info_success :

                    if DEBUG == True :
                        print("RoomFee_Input", RoomFee_Input)

                    room_fee_add_fur = RoomFee_Input+500

                self.clear_form()
                self.on_close()

            else: # If employee not selected
                messagebox.showinfo("Warning", "กรุณากรอกข้อมูลก่อนทำสัญญา")
        else: # If employee not selected
            messagebox.showinfo("Warning", "กรุณาเลือกพนักงานที่ทำสัญญา")

    def on_close(self):
        self.master.deiconify()                        # Show the main page
        self.destroy()

    
    def on_escape(self, event):
        self.on_close()                                # Close the current window