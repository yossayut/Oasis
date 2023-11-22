import tkinter as tk
import sqlite3
import os

from tkinter  import ttk,messagebox, simpledialog
from datetime import datetime, timedelta

from Config.Config       import *

from Contract.CustomerExist                import CustomerExistPage
from Contract.FillCustomerDatabase         import fill_customer_database
from Contract.ContractFillPrepare          import prepare_contract_info, fill_contract_info
from Contract.GetCustomerInfoSubmitForm    import get_customer_info_submit_form
from GetData.GetEmployeeName               import get_employee_name
from GetData.GetCustomerID                 import get_customer_id

#############################################################################################################
# Create ParkingPage, It will show the available parking from Database and if select,
# it will go to the register form
#############################################################################################################
class ParkingRegistrationForm(tk.Toplevel):
    # 1 
    def __init__(self, master, selected_customer):
        super().__init__(master)
        self.title("ลงทะเบียนจอดรถ")
        self.geometry("600x500")
        self.selected_customer = selected_customer
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

        label_plate_no = tk.Label(detail_frame, text="ทะเบียน")
        label_plate_no.grid(row=2, column=0, pady=10)
        self.entry_plate_no   = tk.Entry(detail_frame)
        self.entry_plate_no.focus()
        self.entry_plate_no.grid(row=2, column=1, pady=10)   

        today = datetime.today()
        buddha_year = today.year + 543

        # Format the date as a string with Buddhist year
        formatted_date = today.strftime('%d/%m') + f'/{buddha_year}'

        label_date = tk.Label(detail_frame, text="วันที่ลงทะเบียน")
        label_date.grid(row=3, column=0, pady=10)
        self.entry_date   = tk.Entry(detail_frame)
        self.entry_date.focus()
        self.entry_date.grid(row=3, column=1, pady=10)  
        self.entry_date.insert(0, formatted_date) 

        ##########################################################################################
        ok_button = tk.Button(self, text="OK", command=self.record_data)
        ok_button.grid(row=7, column=1, columnspan=2, pady=20)

        self.columnconfigure(1, weight=1)

    # 4 : 
    def clear_form(self):
        self.entry_brand_model.config(state=tk.NORMAL)
        self.entry_color.config(state=tk.NORMAL)
        self.entry_plate_no.config(state=tk.NORMAL)

        # Clear other fields as needed
        self.entry_brand_model.delete(0, tk.END)
        self.entry_color.delete(0, tk.END)
        self.entry_plate_no.delete(0, tk.END)

    def record_data(self):
        get_Brand_model    = self.entry_brand_model.get()             # Get Brand/ Model
        get_Color          = self.entry_color.get()                   # Get Color
        get_Plate_no       = self.entry_plate_no.get()                # Get Plate No.
        get_Date           = self.entry_date.get()                    # Retrieve the value from the Entry widget
        get_Date           = datetime.strptime(get_Date, '%d/%m/%Y')  # Convert string to datetime

        customer_name       = self.selected_customer
        customer_name_parts = customer_name.split(" ")

        if DEBUG == True :
            print(customer_name)        
            print(customer_name_parts)
            print(customer_name_parts[0])
            print(customer_name_parts[1])
        
        get_CustomerID              = get_customer_id(customer_name_parts[0],customer_name_parts[1])

        if DEBUG == True :        
            print(get_CustomerID)
        
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        try:
            ##########################################################################################
            #   Car Parking                                                                          #
            ##########################################################################################
            if self.automotive_type.get() == "car" :
                if DEBUG == True :
                    print("เลือก car")  

                cursor.execute("""
                    INSERT INTO Car_TBL(Brand_Model, Color, PlateNo, CustomerID, RegisterDate)
                    VALUES (?,?,?,?,?)
                """,(get_Brand_model, get_Color, get_Plate_no, get_CustomerID, get_Date))   

                conn.commit()
                conn.close()

                self.after_transaction(get_Brand_model, get_Plate_no, "ลงทะเบียนรถยนต์เรียบร้อย")

            ##########################################################################################
            #   Motocycle Parking                                                                    #
            ##########################################################################################
            elif self.automotive_type.get() == "motocycle" : 
                if DEBUG == True :
                    print("เลือก motocycle") 

                cursor.execute("""
                    INSERT INTO Motocycle_TBL(Brand_Model, Color, PlateNo, CustomerID, RegisterDate)
                    VALUES (?,?,?,?,?)
                """,(get_Brand_model, get_Color, get_Plate_no, get_CustomerID, get_Date))   

                conn.commit()
                conn.close()

                self.after_transaction(get_Brand_model, get_Plate_no, "ลงทะเบียนมอเตอร์ไซต์เรียบร้อย")

            ##########################################################################################
            #                                                                                        #
            ##########################################################################################
            else :
                print("no")


        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()

    def after_transaction(self, card_number, staff_name, transaction_type):
        message = f"Transaction Successful!\nรถ: {card_number}\nทะเบียน: {staff_name}\nTransaction Type: {transaction_type}"
        messagebox.showinfo("Transaction Info", message)
        self.destroy()  # Closes the current window
        self.master.deiconify()  # Show the main page

    def on_close(self):
        self.master.deiconify()                        # Show the main page
        self.destroy()

    
    def on_escape(self, event):
        self.on_close()                                # Close the current window