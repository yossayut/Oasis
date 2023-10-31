import tkinter as tk
import sqlite3

from tkinter  import messagebox, simpledialog
from datetime import datetime, timedelta
from docxtpl  import DocxTemplate

from Config.Config       import *

from Contract.CustomerExist       import CustomerExistPage

from Contract.ContractFillPrepare import prepare_contract_info, fill_contract_info
from GetData.GetEmployeeName     import get_employee_name

global new_customer_flag

#############################################################################################################
# Create ParkingPage, It will show the available parking from Database and if select,
# it will go to the register form
#############################################################################################################
class RegistrationForm(tk.Toplevel):
    # 1 
    def __init__(self, master, room):
        super().__init__(master)
        self.title("ลงทะเบียนลูกค้าใหม่")
        self.geometry("600x500")
        self.room = room
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind('<Escape>', self.on_escape)
        self.new_customer_flag = True                      # Initialize new customer as True

    # 2
    def create_widgets(self):
        ##################################################
        # Create entry box variable
        ##################################################
        self.prefix_entry               = tk.Entry(self)
        self.first_name_entry           = tk.Entry(self)
        self.last_name_entry            = tk.Entry(self)
        self.nick_name_entry            = tk.Entry(self)
        self.national_ID_entry          = tk.Entry(self)
        self.birthday_entry             = tk.Entry(self)
        self.address_entry              = tk.Entry(self)
        self.address_cont_entry         = tk.Entry(self)
        self.address_road_entry         = tk.Entry(self)
        self.address_sub_province_entry = tk.Entry(self)
        self.address_province_entry     = tk.Entry(self)
        self.address_city_entry         = tk.Entry(self)
        self.phone_entry                = tk.Entry(self)
        self.lineID_entry               = tk.Entry(self)
        self.job_entry                  = tk.Entry(self)
        self.emergency_entry            = tk.Entry(self)
        self.register_date_entry        = tk.Entry(self)
        self.register_end_date_entry    = tk.Entry(self)
        self.room_fee_entry             = tk.Entry(self)
        self.internet_fee_entry         = tk.Entry(self)
        self.maintenance_fee_entry      = tk.Entry(self)
        self.parking_fee_entry          = tk.Entry(self)
        self.remark_entry               = tk.Entry(self)

        ########################################################################################################
        # Old customer box : ต่ออายุสัญญาหลังจากครบครั้งแรกแล้ว เลยไม่ต้องกรอกข้อมูลผู้เช่าใหม่
        ########################################################################################################
        tk.Button(self, text="ลูกค้าเก่า", command=self.open_exist_customer).grid(row=0, column=1, pady=10)

        ########################################################################################################
        # Drop down employee name : Filler PIC
        ########################################################################################################
        self.employee_names = get_employee_name()                                                  # employee name
        if DEBUG == True :
            print(self.employee_names)

        tk.Label(self, text="พนักงาน   :").grid(row=0, column=3)     
        self.selected_employee = tk.StringVar()
        self.selected_employee.set("กรุณาเลือกพนักงาน") 
        self.employee_dropdown = tk.OptionMenu(self, self.selected_employee, *self.employee_names)
        self.employee_dropdown.grid(row=0, column=4)

        ########################################################################################################
        # Create entry box + button position
        ########################################################################################################
        tk.Label(self, text="หมายเลขห้องทำสัญญา  :").grid(row=1, column=0)                        # Room No.
        tk.Label(self, text=self.room).grid(row=1, column=1)

        tk.Label(self, text="คำนำหน้าชื่อ  :").grid(row=2, column=0)                              # Prefix
        self.prefix_entry = tk.Entry(self)
        self.prefix_entry.grid(row=2, column=1)

        tk.Label(self, text="ชื่อ   :  ").grid(row=3, column=0)                                   # Name
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.grid(row=3, column=1)

        tk.Label(self, text="นามสกุล   :  ").grid(row=4, column=0)                               # Last name
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.grid(row=4, column=1)

        tk.Label(self, text="ชื่อเล่น   :  ").grid(row=5, column=0)                                # Nick name
        self.nick_name_entry = tk.Entry(self)
        self.nick_name_entry.grid(row=5, column=1)

        tk.Label(self, text="เลขบัตรประชาชน x-xxxx-xxxxx-xx-x  :  ").grid(row=6, column=0)        # ID
        self.national_ID_entry = tk.Entry(self)
        self.national_ID_entry.grid(row=6, column=1)

        tk.Label(self, text="วัน/เดือน/ปี เกิด (วว/ดด/ปปปป)   :  ").grid(row=7, column=0)            # Birth day
        self.birthday_entry = tk.Entry(self)
        self.birthday_entry.grid(row=7, column=1)

        tk.Label(self, text="ที่อยู่เลขที่   :  ").grid(row=8, column=0)                              # Address
        self.address_entry = tk.Entry(self)
        self.address_entry.grid(row=8, column=1)

        tk.Label(self, text="ที่อยู่ (ต่อ)   :  ").grid(row=9, column=0)                             # Address Continue
        self.address_cont_entry = tk.Entry(self)
        self.address_cont_entry.grid(row=9, column=1)

        tk.Label(self, text="ถนน   :  ").grid(row=10, column=0)                                 # Address Road
        self.address_road_entry = tk.Entry(self)
        self.address_road_entry.grid(row=10, column=1)

        tk.Label(self, text="แขวง / ตำบล   :  ").grid(row=11, column=0)                         # Address sub Province
        self.address_sub_province_entry = tk.Entry(self)
        self.address_sub_province_entry.grid(row=11, column=1)

        tk.Label(self, text="เขต / อำเภอ   :  ").grid(row=12, column=0)                         # Address Province   
        self.address_province_entry = tk.Entry(self)
        self.address_province_entry.grid(row=12, column=1)

        tk.Label(self, text="จังหวัด   :  ").grid(row=13, column=0)                               # Address City
        self.address_city_entry = tk.Entry(self)
        self.address_city_entry.grid(row=13, column=1)

        tk.Label(self, text="เบอร์โทร   :  ").grid(row=14, column=0)                              # Phone
        self.phone_entry = tk.Entry(self)            
        self.phone_entry.grid(row=14, column=1)

        tk.Label(self, text="LineID   :  ").grid(row=15, column=0)                              # Line ID
        self.lineID_entry = tk.Entry(self)
        self.lineID_entry.grid(row=15, column=1)

        tk.Label(self, text="อาชีพ   :  ").grid(row=16, column=0)                                # Job
        self.job_entry = tk.Entry(self)
        self.job_entry.grid(row=16, column=1)

        tk.Label(self, text="ติดต่อฉุกเฉิน   :  ").grid(row=17, column=0)                           # 
        self.emergency_entry = tk.Entry(self)
        self.emergency_entry.grid(row=17, column=1)

        tk.Label(self, text="เริ่มต้นสัญญาวันที่   :  ").grid(row=18, column=0)
        self.register_date_entry = tk.Entry(self)
        self.register_date_entry.grid(row=18, column=1)
        today = datetime.today().strftime('%Y-%m-%d')   # Set default value for register date to today 
        self.register_date_entry.insert(0, today)

        tk.Label(self, text=" สิ้นสุดสัญญาวันที่   :  ").grid(row=19, column=0)
        self.register_end_date_entry = tk.Entry(self)
        self.register_end_date_entry.grid(row=19, column=1)
        today = datetime.today()
        six_months_from_now = today + timedelta(days=6*30)
        default_date  = six_months_from_now.strftime('%Y-%m-%d')   # Set default value for register date to today 
        self.register_end_date_entry.insert(0, default_date)

        ########################################################################################################
        # Create button : submit button
        ########################################################################################################
        tk.Button(self, text="สร้างสัญญาเช่า", command=self.submit_form).grid(row=20, column=1, pady=10)
        ########################################################################################################

    # 3 : Run
    def open_exist_customer(self):
        self.clear_form()
        self.new_customer_flag = False                                  # Reset flag for existing customer
        if DEBUG == True :
            print("open_exist_customer : ",self.new_customer_flag)

        ####################################################
        # Call : CustomerexistPage CustomerexistPage.py
        ####################################################
        exist_page = CustomerExistPage(self)
        exist_page.wait_window()
        customer_info = exist_page.get_selected_customer_info()

    # 4 : 
    def clear_form(self):
        self.prefix_entry.config(state=tk.NORMAL)
        self.first_name_entry.config(state=tk.NORMAL)
        self.last_name_entry.config(state=tk.NORMAL)
        self.nick_name_entry.config(state=tk.NORMAL)
        self.national_ID_entry.config(state=tk.NORMAL)
        self.birthday_entry.config(state=tk.NORMAL)
        self.address_entry.config(state=tk.NORMAL)
        self.address_cont_entry.config(state=tk.NORMAL)
        self.address_road_entry.config(state=tk.NORMAL)
        self.address_sub_province_entry.config(state=tk.NORMAL)
        self.address_province_entry.config(state=tk.NORMAL)
        self.address_city_entry.config(state=tk.NORMAL)
        self.phone_entry.config(state=tk.NORMAL)
        self.lineID_entry.config(state=tk.NORMAL)
        self.job_entry.config(state=tk.NORMAL)
        self.emergency_entry.config(state=tk.NORMAL)
        self.register_date_entry.config(state=tk.NORMAL)
        self.register_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        # Clear other fields as needed
        self.prefix_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.nick_name_entry.delete(0, tk.END)
        self.national_ID_entry.delete(0, tk.END)
        self.birthday_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.address_cont_entry.delete(0, tk.END)
        self.address_road_entry.delete(0, tk.END)
        self.address_sub_province_entry.delete(0, tk.END)
        self.address_province_entry.delete(0, tk.END)
        self.address_city_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.lineID_entry.delete(0, tk.END)
        self.job_entry.delete(0, tk.END)
        self.emergency_entry.delete(0, tk.END)
        self.register_date_entry.delete(0, tk.END)
        self.register_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        today = datetime.today()
        six_months_from_now = today + timedelta(days=6*30)
        default_date = six_months_from_now.strftime('%Y-%m-%d')
        self.register_end_date_entry.delete(0, tk.END)
        self.register_end_date_entry.insert(0, default_date)

        # 8           

    # 5
    def fill_customer_exist_info(self, customer_info):
        if DEBUG == True :
            print("fill_customer_exist_info : CustomerRegistrationForm.py")

        ################################################################
        # Fill the entry fields with the provided customer information
        ################################################################
        self.prefix_entry.delete(0, tk.END)
        self.prefix_entry.insert(0, customer_info[1])
        self.prefix_entry.config(state=tk.DISABLED)

        self.first_name_entry.delete(0, tk.END)
        self.first_name_entry.insert(0, customer_info[2])
        self.first_name_entry.config(state=tk.DISABLED)

        self.last_name_entry.delete(0, tk.END)
        self.last_name_entry.insert(0, customer_info[3])
        self.last_name_entry.config(state=tk.DISABLED)

        self.nick_name_entry.delete(0, tk.END)
        self.nick_name_entry.insert(0, customer_info[4])
        self.nick_name_entry.config(state=tk.DISABLED)

        self.national_ID_entry.delete(0, tk.END)
        self.national_ID_entry.insert(0, customer_info[5])
        self.national_ID_entry.config(state=tk.DISABLED)

        self.birthday_entry.delete(0, tk.END)
        self.birthday_entry.insert(0, customer_info[6])
        self.birthday_entry.config(state=tk.DISABLED)

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, customer_info[7])
        self.address_entry.config(state=tk.DISABLED)

        self.address_cont_entry.delete(0, tk.END)
        self.address_cont_entry.insert(0, customer_info[8])
        self.address_cont_entry.config(state=tk.DISABLED)

        self.address_road_entry.delete(0, tk.END)
        self.address_road_entry.insert(0, customer_info[9])
        self.address_road_entry.config(state=tk.DISABLED)

        self.address_sub_province_entry.delete(0, tk.END)
        self.address_sub_province_entry.insert(0, customer_info[10])
        self.address_sub_province_entry.config(state=tk.DISABLED)

        self.address_province_entry.delete(0, tk.END)
        self.address_province_entry.insert(0, customer_info[11])
        self.address_province_entry.config(state=tk.DISABLED)

        self.address_city_entry.delete(0, tk.END)
        self.address_city_entry.insert(0, customer_info[12])
        self.address_city_entry.config(state=tk.DISABLED)

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, customer_info[13])
        self.phone_entry.config(state=tk.DISABLED)

        self.lineID_entry.delete(0, tk.END)
        self.lineID_entry.insert(0, customer_info[14])
        self.lineID_entry.config(state=tk.DISABLED)

        self.job_entry.delete(0, tk.END)
        self.job_entry.insert(0, customer_info[15])
        self.job_entry.config(state=tk.DISABLED)

        self.emergency_entry.delete(0, tk.END)
        self.emergency_entry.insert(0, customer_info[16])
        self.emergency_entry.config(state=tk.DISABLED)

    # 6
    def submit_form(self):

        #print("submit_form")
        ####################################################
        # Get information from text box
        ####################################################
        selected_room         = self.room
        prefix                = self.prefix_entry.get()
        first_name            = self.first_name_entry.get()
        last_name             = self.last_name_entry.get()
        nick_name             = self.nick_name_entry.get()
        thai_national_id      = self.national_ID_entry.get()
        birth_day             = self.birthday_entry.get()
        address_number        = self.address_entry.get()
        address_cont          = self.address_cont_entry.get()
        address_road          = self.address_road_entry.get()
        address_sub_province  = self.address_sub_province_entry.get()
        address_province      = self.address_province_entry.get()
        address_city          = self.address_city_entry.get()
        phone                 = self.phone_entry.get()
        line_id               = self.lineID_entry.get()
        job                   = self.job_entry.get()
        emergency             = self.emergency_entry.get()
        register_date         = self.register_date_entry.get()
        register_end_date     = self.register_end_date_entry.get()

        ####################################################
        # Get information from text box : Column2
        ####################################################       
        employee              = self.selected_employee.get()
        room_fee              = self.room_fee_entry.get()  
        internet              = self.internet_fee_entry.get()
        maintenance           = self.maintenance_fee_entry.get()
        parking               = self.parking_fee_entry.get()
        remark                = self.remark_entry.get()

        if DEBUG == True :
            print("employee : " + employee)
            name_parts = employee.strip("()").split(", ")
            # Extract the individual names
            first_name_employee = name_parts[0]
            last_name_employee = name_parts[1]
            print("first name : " + first_name_employee)
            print("last name : " + last_name_employee)

        # Store the data in the database
        conn = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()
        if DEBUG == True :
            print("submit_form (new customer ?) : ", self.new_customer_flag)
        
        #########################################################
        # If employee not selected
        #########################################################       
        if employee != "กรุณาเลือกพนักงาน" :

            #########################################################
            # new customer, add customer information to database
            #########################################################
            if self.new_customer_flag:
                #print("New customer add to Database")
                try:
                    # Insert data into the table
                    sql = """
                        INSERT INTO Customer_TBL 
                        (Prefix, FirstName, LastName, NickName, ThaiNationalID, BirthDay, AddressNumber, AddressCont,
                        AddressRoad, AddressSubProvince, AddressProvince, AddressCity, Phone, LineID, Job, ReferencePerson, RegisterDate)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    
                    # Parameters for the query
                    params = (prefix, first_name, last_name, nick_name, thai_national_id, 
                        birth_day, address_number, address_cont, address_road, 
                        address_sub_province, address_province, address_city, 
                        phone, line_id, job, emergency, register_date)

                    conn.execute(sql, params)
                    conn.commit()
                    clear_form()
                    database.show_all(Oasis_database_full_path,'Customer_TBL')
                    messagebox.showinfo("Success", "Customer information added successfully.")

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

                finally:
                    # Close the database connection
                    if conn:
                        conn.close()

            else:  # Old customer
                messagebox.showinfo("ลูกค้าเก่า", "ลูกค้าเก่า")

            ##################################################################################################################
            # Get contract information : ContractInformation.py
            # Prepare all information before fill contract database 
            # ex. 
            #     room information      from Apartment_Info_TBL
            #     customer information  from Customer_TBL
            #     employee name         from Employee_TBL
            ##################################################################################################################         
            contract_info = prepare_contract_info(selected_room, first_name, last_name, register_date, register_end_date, employee,
                                                  room_fee, internet, maintenance, parking, remark)
            #print(contract_info)

            #########################################################
            # Fill contract to Database : ContractInformation.py
            # Fill Contract information to Contract_TBL
            #########################################################   
            if contract_info :
                RoomID_Input, RoomType_Input, CustomerID_Input, StartDate_Input, EndDate_Input, employeeID_Input, RoomFee_Input, \
                InternetFee_Input, MaintenanceFee_Input, ParkingFee_Input, Remark_Input, Status_Input = contract_info                 # Unpack contract info

                if RoomType_Input == 'SmallType':
                    room_fee = '3,500'

                elif RoomType_Input == 'BigType':
                    room_fee = '4,000'

                else :
                    print('error Room out of scope')

                room_floor    = selected_room[1]
                room_building = selected_room[0]

                fill_contract_info(RoomID_Input, CustomerID_Input, StartDate_Input, EndDate_Input, employeeID_Input, RoomFee_Input,
                                   InternetFee_Input, MaintenanceFee_Input, ParkingFee_Input, Remark_Input, Status_Input)

                ###############################################################################
                # Fill contract to contract file (Word) C:\Database\สัญญาเช่าอะพาร์ตเมนต์.docx")
                ###############################################################################   
                doc = DocxTemplate(template_contract_path)
                context = { 'วันที่'            : StartDate_Input ,
                            'คำนำหน้า'        : prefix,
                            'ชื่อ'             : first_name,
                            'นามสกุล'         : last_name,
                            'บ้านเลขที่'        : address_number,
                            'บ้านเลขที่ต่อ'      : address_cont,
                            'ถนน'            : address_road,
                            'ตำบล'           : address_sub_province,
                            'อำเภอ'           : address_province,
                            'จังหวัด'           : address_city,
                            'เบอร์โทร'         :  phone,
                            'ติดต่อฉุกเฉิน'      : emergency,
                            'ห้องพักเลขที่'      : selected_room,
                            'ชั้นที่'           : room_floor,
                            'อาคาร'          : room_building,
                            'ค่าเช่า'          : room_fee,
                            'วันเริ่มสัญญา'     : register_date,
                            'วันสิ้นสุดสัญญา'  : register_end_date,
                            'ผู้กรอกข้อมูล'    : employee
                        }
                doc.render(context)
                doc.save(output_contract_path)

            self.clear_form()
            self.on_close()

        else: # If employee not selected
            messagebox.showinfo("Warning", "กรุณาเลือกพนักงานก่อน")

    # 7
    def on_close(self):
        if DEBUG == True :
            print("onclose", self.new_customer_flag)

        self.new_customer_flag = True                  # Reset flag for existing customer

        if DEBUG == True :
            print("onclose after set", self.new_customer_flag)

        self.master.deiconify()                        # Show the main page
        self.destroy()

    
    def on_escape(self, event):
        self.on_close()                                # Close the current window