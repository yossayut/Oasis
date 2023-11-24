import tkinter as tk
import sqlite3
import os

from tkinter  import messagebox, simpledialog
from datetime import datetime, timedelta
from docxtpl  import DocxTemplate
from docx     import Document

from Config.Config                         import *
from Contract.CustomerExist                import CustomerExistPage
from Contract.FillCustomerDatabase         import fill_customer_database
from Contract.ContractFillPrepare          import prepare_contract_info, fill_contract_info
from Contract.GetCustomerInfoSubmitForm    import get_customer_info_submit_form
from GetData.GetEmployeeName               import get_employee_name_from_DB

global new_customer_flag

#############################################################################################################
# Create ParkingPage, It will show the available parking from Database and if select,
# it will go to the register form
#############################################################################################################
class RegistrationForm(tk.Toplevel):
    def __init__(self, master, room):
        super().__init__(master)
        self.title("ลงทะเบียนลูกค้าใหม่")
        self.geometry("600x500")
        self.room = room
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind('<Escape>', self.on_escape)
        self.new_customer_flag = True                      # Initialize new customer as True

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

        txt_button_exist_customer       = "ลูกค้าเก่า"
        txt_staff                       = "พนักงาน   :"
        txt_select_staff                = "กรุณาเลือกพนักงาน"
        txt_contract_room               = "หมายเลขห้องทำสัญญา  :"
        txt_prefix                      = "คำนำหน้าชื่อ  :"
        txt_customer_first_name         = "ชื่อ   :  "
        txt_customer_last_name          = "นามสกุล   :  "
        txt_customer_nick_name          = "ชื่อเล่น   :  "
        txt_customer_id                 = "เลขบัตรประชาชน x-xxxx-xxxxx-xx-x  :  "
        txt_customer_birth_day          = "วัน/เดือน/ปี เกิด (วว/ดด/ปปปป)   :  "

        txt_address                     = "ที่อยู่เลขที่   :  "
        txt_address_cont                = "ที่อยู่ (ต่อ)   :  "
        txt_road                        = "ถนน   :  "
        txt_sub_province                = "แขวง / ตำบล   :  "
        txt_province                    = "เขต / อำเภอ   :  "
        txt_city                        = "จังหวัด   :  "
        txt_tel_no                      = "เบอร์โทร   :  "
        txt_lineid                      = "LineID   :  "
        txt_job                         = "อาชีพ   :  "
        txt_emergency_contact           = "ติดต่อฉุกเฉิน (ชื่อ เบอร์โทร ความสัมพันธ์) :  "
        txt_start_contract              = "เริ่มต้นสัญญาวันที่   :  "
        txt_end_contract                = "สิ้นสุดสัญญาวันที่   :  "
        txt_button_contract             = "ทำสัญญาเช่า"
        txt_button_booking              = "จองห้อง" 

        ########################################################################################################
        # Old customer box : ต่ออายุสัญญาหลังจากครบครั้งแรกแล้ว เลยไม่ต้องกรอกข้อมูลผู้เช่าใหม่
        ########################################################################################################
        tk.Button(self, text=txt_button_exist_customer, command=self.open_exist_customer).grid(row=0, column=1, pady=10)

        ########################################################################################################
        # Drop down employee name : Filler PIC
        ########################################################################################################
        self.employee_names = get_employee_name_from_DB()                             # employee name
        if DEBUG == True :
            print(self.employee_names)
        tk.Label(self, text=txt_staff).grid(row=0, column=3)     
        self.selected_employee = tk.StringVar()
        self.selected_employee.set(txt_select_staff) 
        self.employee_dropdown = tk.OptionMenu(self, self.selected_employee, *self.employee_names)
        self.employee_dropdown.grid(row=0, column=4)

        ########################################################################################################
        # Create entry box + button position
        ########################################################################################################
        tk.Label(self, text=txt_contract_room).grid(row=1, column=0)                  # Room No.
        tk.Label(self, text=self.room).grid(row=1, column=1)

        tk.Label(self, text=txt_prefix).grid(row=2, column=0)                         # Prefix
        self.prefix_entry = tk.Entry(self)
        self.prefix_entry.grid(row=2, column=1)

        tk.Label(self, text=txt_customer_first_name).grid(row=3, column=0)            # Name
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.grid(row=3, column=1)

        tk.Label(self, text=txt_customer_last_name).grid(row=4, column=0)             # Last name
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.grid(row=4, column=1)

        tk.Label(self, text=txt_customer_nick_name).grid(row=5, column=0)             # Nick name
        self.nick_name_entry = tk.Entry(self)
        self.nick_name_entry.grid(row=5, column=1)

        tk.Label(self, text=txt_customer_id).grid(row=6, column=0)                    # ID
        self.national_ID_entry = tk.Entry(self)
        self.national_ID_entry.grid(row=6, column=1)

        tk.Label(self, text=txt_customer_birth_day).grid(row=7, column=0)             # Birth day
        self.birthday_entry = tk.Entry(self)
        self.birthday_entry.grid(row=7, column=1)

        tk.Label(self, text=txt_address).grid(row=8, column=0)                        # Address
        self.address_entry = tk.Entry(self)
        self.address_entry.grid(row=8, column=1)

        tk.Label(self, text=txt_address_cont).grid(row=9, column=0)                   # Address Continue
        self.address_cont_entry = tk.Entry(self)
        self.address_cont_entry.grid(row=9, column=1)

        tk.Label(self, text=txt_road).grid(row=10, column=0)                          # Address Road
        self.address_road_entry = tk.Entry(self)
        self.address_road_entry.grid(row=10, column=1)

        tk.Label(self, text=txt_sub_province).grid(row=11, column=0)                  # Address sub Province
        self.address_sub_province_entry = tk.Entry(self)
        self.address_sub_province_entry.grid(row=11, column=1)

        tk.Label(self, text=txt_province).grid(row=12, column=0)                      # Address Province   
        self.address_province_entry = tk.Entry(self)
        self.address_province_entry.grid(row=12, column=1)

        tk.Label(self, text=txt_city).grid(row=13, column=0)                          # Address City
        self.address_city_entry = tk.Entry(self)
        self.address_city_entry.grid(row=13, column=1)

        tk.Label(self, text=txt_tel_no).grid(row=14, column=0)                        # Phone
        self.phone_entry = tk.Entry(self)            
        self.phone_entry.grid(row=14, column=1)

        tk.Label(self, text=txt_lineid).grid(row=15, column=0)                        # Line ID
        self.lineID_entry = tk.Entry(self)
        self.lineID_entry.grid(row=15, column=1)

        tk.Label(self, text=txt_job).grid(row=16, column=0)                           # Job
        self.job_entry = tk.Entry(self)
        self.job_entry.grid(row=16, column=1)

        tk.Label(self, text=txt_emergency_contact).grid(row=17, column=0)             # Emergency contact
        self.emergency_entry = tk.Entry(self)
        self.emergency_entry.grid(row=17, column=1)

        tk.Label(self, text=txt_start_contract).grid(row=18, column=0)                # Start
        self.register_date_entry = tk.Entry(self)
        self.register_date_entry.grid(row=18, column=1)
        today = datetime.today()
        buddha_year = today.year + 543

        # Format the date as a string with Buddhist year
        formatted_date = today.strftime('%d/%m') + f'/{buddha_year}'
        self.register_date_entry.insert(0, formatted_date)

        tk.Label(self, text=txt_end_contract).grid(row=19, column=0)
        self.register_end_date_entry = tk.Entry(self)
        self.register_end_date_entry.grid(row=19, column=1)                           # End
        
        six_months_from_now = today + timedelta(days=6*30)
        end_of_month        = (six_months_from_now.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        default_date        = end_of_month.strftime('%d/%m') + f'/{buddha_year}'      
        self.register_end_date_entry.insert(0, default_date)

        ########################################################################################################
        # Create button : Contract submit button
        ########################################################################################################
        tk.Button(self, text=txt_button_contract, command=lambda: self.submit_form("contract")).grid(row=20, column=1, pady=10)

        ########################################################################################################
        # Create button : Booking submit button
        ########################################################################################################
        tk.Button(self, text=txt_button_booking, command=lambda: self.submit_form("booking")).grid(row=20, column=2, pady=10)

    def open_exist_customer(self):
        self.clear_form()
        self.new_customer_flag = False # Reset flag for existing customer

        if DEBUG == True :
            print("open_exist_customer => self.new_customer_flag : ", self.new_customer_flag)

        exist_page    = CustomerExistPage(self)
        exist_page.wait_window()
        customer_info = exist_page.get_selected_customer_info()

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
        self.register_end_date_entry.delete(0, tk.END)

        today          = datetime.today()
        buddha_year    = today.year + 543
        formatted_date = today.strftime('%d/%m') + f'/{buddha_year}'
        self.register_date_entry.insert(0, formatted_date)

        six_months_from_now = today + timedelta(days=6*30)
        end_of_month        = (six_months_from_now.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        default_date        = end_of_month.strftime('%d/%m') + f'/{buddha_year}'  # Assuming you want the year in the format YYYY
        self.register_end_date_entry.insert(0, default_date)

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

    def submit_form(self, form_type):
        if DEBUG == True :
            print("submit_form")
            print("submit_form => form_type : ", form_type)

        data = get_customer_info_submit_form(self) 

        if DEBUG == True :
            print("submit_form => data : ", data)

        selected_room, prefix, first_name, last_name, nick_name, thai_national_id, birth_day, address_number, address_cont, \
        address_road, address_sub_province, address_province, address_city, phone, line_id, job, emergency, register_date,  \
        register_end_date, employee, room_fee, internet, maintenance, parking, remark = data
  
        if first_name != "" or last_name != "" or thai_national_id != "" :
            # Check some txt box not empty then process
            if employee != "กรุณาเลือกพนักงาน":
                # new customer
                if self.new_customer_flag:
                    inserted = fill_customer_database(prefix, first_name, last_name, nick_name, thai_national_id, birth_day, 
                        address_number, address_cont, address_road, address_sub_province, address_province, address_city, phone, 
                        line_id, job, emergency, register_date)
                    
                    if inserted:
                        self.clear_form()
                # old customer
                else:
                    messagebox.showinfo("ลูกค้าเก่า", "ลูกค้าเก่า")
        
                contract_info = prepare_contract_info(selected_room, first_name, last_name, register_date, register_end_date, employee,
                                                      remark)

                employee_names      = employee.strip("()").split(", ")
                employee_first_name = employee_names[0].strip("'")       # Extract the first name
                employee_last_name  = employee_names[1].strip("'")       # Extract the second name
                employee_name       = employee_first_name + ' ' + employee_last_name

                if DEBUG == True :
                    print("contract_submit_form => employee_name : " + employee_name)
                    print("contract_submit_form => contract_info : ", contract_info)

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
                flag_fill_contract_info_success = fill_contract_info(form_type, RoomID_Input, CustomerID_Input, StartDate_Input, EndDate_Input, employeeID_Input, RoomFee_Input,
                                                                     InternetFee_Input, MaintenanceFee_Input, ParkingFee_Input, Remark_Input, Status_Input)

                if flag_fill_contract_info_success :

                    if DEBUG == True :
                        print("contract_submit_form => RoomFee_Input : ", RoomFee_Input)

                    room_fee_add_fur = RoomFee_Input + 500

                    if DEBUG == True :
                        print("contract_submit_form => room_fee_add_fur : ", room_fee_add_fur)

                    if form_type == "contract" :
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
                                    'ค่าเช่า'          : RoomFee_Input,
                                    'ค่าเช่ารวมเฟอร์'    : room_fee_add_fur,
                                    'วันเริ่มสัญญา'     : register_date,
                                    'วันสิ้นสุดสัญญา'   : register_end_date,
                                    'ผู้กรอกข้อมูล'     : employee_name,
                                    'ไลน์id'         : line_id
                                }
                        doc.render(context)
                        doc.save(output_contract_path)

                        Document(output_contract_path)
                        os.startfile(output_contract_path)
                    
                    else :
                        messagebox.showinfo("พริ้นท์ใบจอง", "พริ้นท์ใบจอง")

                self.clear_form()
                self.on_close()

            else: 
                # If employee not selected
                messagebox.showinfo("Warning", "กรุณาเลือกพนักงานที่ทำสัญญา")
        else: 
            # If employee not selected
            messagebox.showinfo("Warning", "กรุณากรอกข้อมูลก่อนทำสัญญา") 

    def on_close(self):
        self.new_customer_flag = True                  # Reset flag for existing customer
        self.master.deiconify()                        # Show the main page
        self.destroy()

    def on_escape(self, event):
        self.on_close()                                # Close the current window