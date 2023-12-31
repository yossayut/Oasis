import sqlite3

from Config.Config         import *
from tkinter               import messagebox
from GetData.GetEmployeeID import get_employee_id_from_first_last_name
from docxtpl               import DocxTemplate
from docx                  import Document

####################################################
# Get information from Database
####################################################
def prepare_contract_info(selected_room, first_name, last_name, register_date, register_end_date, employee, remark):
    try:
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        cursor.execute("SELECT RoomID FROM Apartment_Info_TBL WHERE RoomNo = ?", (selected_room,))
        RoomID_Input     = cursor.fetchone()[0]

        cursor.execute("SELECT RoomType FROM Apartment_Info_TBL WHERE RoomNo = ?", (selected_room,))
        RoomType_Input   = cursor.fetchone()[0]

        cursor.execute("SELECT CustomerID FROM Customer_TBL WHERE FirstName = ? AND LastName = ?", (first_name, last_name,))
        CustomerID_Input = cursor.fetchone()[0]

        StartDate_Input  = register_date
        EndDate_Input    = register_end_date

        name_parts       = employee.strip("()").replace("'", "").split(", ")

        if DEBUG == True :
            print("prepare_contract_info => name_parts[0] : " + name_parts[0])
            print("prepare_contract_info => name_parts[1] : " + name_parts[1])

        EmployeeID_Input     = get_employee_id_from_first_last_name(name_parts[0],name_parts[1])

        if RoomType_Input == 'SmallType':
            room_fee = 3500

        elif RoomType_Input == 'BigType':
            room_fee = 4000

        else :
            print('error Room out of scope')


        RoomFee_Input        = room_fee
        InternetFee_Input    = 0    
        MaintenanceFee_Input = 0
        ParkingFee_Input     = 0
        Remark_Input         = remark
        Status_Input         = "Active"

        return RoomID_Input,           \
               RoomType_Input,         \
               CustomerID_Input,       \
               StartDate_Input,        \
               EndDate_Input,          \
               EmployeeID_Input,       \
               RoomFee_Input,          \
               InternetFee_Input,      \
               MaintenanceFee_Input,   \
               ParkingFee_Input,       \
               Remark_Input,           \
               Status_Input

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return None

    finally:
        if conn:
            conn.close()

#########################################################
# Fill contract to Database
#########################################################  
def fill_contract_info(form_type, RoomID_Input, CustomerID_Input, StartDate_Input, EndDate_Input, EmployeeID_Input, RoomFee_Input, InternetFee_Input, MaintenanceFee_Input, ParkingFee_Input, Remark_Input, Status_Input):
    if DEBUG == True :
       print("fill_contract_info => form_type : " + form_type) 

    if form_type == "contract" :
        if DEBUG == True :
           print("form_type == contract")

        try:
            conn   = sqlite3.connect(Oasis_database_full_path)
            cursor = conn.cursor()

            cursor.execute(""" 
                               SELECT *
                               FROM  Contract_TBL
                               WHERE Contract_TBL.RoomID = (?) AND Contract_TBL.Status = 'Active'
                               UNION
                               SELECT *
                               FROM  Booking_TBL
                               WHERE Booking_TBL.RoomID = (?) AND Booking_TBL.Status = 'Active'

                           """ ,(RoomID_Input,RoomID_Input,))

            result = cursor.fetchall()

            if result:
                check_booking_contract_active = True
            else:
                check_booking_contract_active = False          

            if not check_booking_contract_active :
                cursor.execute(""" INSERT INTO Contract_TBL (RoomID, 
                                                             CustomerID,
                                                             StartDate,
                                                             EndDate,
                                                             StaffID,
                                                             RoomFee,
                                                             InternetFee,
                                                             MaintenanceFee,
                                                             ParkingFee,
                                                             Remark,
                                                             Status) 
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               """, (RoomID_Input, CustomerID_Input, StartDate_Input, EndDate_Input, EmployeeID_Input, RoomFee_Input,
                                     InternetFee_Input, MaintenanceFee_Input, ParkingFee_Input, Remark_Input, Status_Input))

                conn.commit()
                messagebox.showinfo("Success", "สัญญาเสร็จสมบูรณ์ กรุณาปริ้นท์เอกสารสัญญาลงนาม")
                flag_fill_info_success = True
                return flag_fill_info_success

            else :
                messagebox.showinfo("Warning", "ห้องที่ต้องการติดจองหรือติดสัญญาอยู่ กรุณาเลือกห้องอื่น")
                flag_fill_info_success = False
                return flag_fill_info_success

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()

    # booking
    elif form_type == "booking" :
        if DEBUG == True :
           print("form_type == booking")

        try:
            conn   = sqlite3.connect(Oasis_database_full_path)
            cursor = conn.cursor()

            cursor.execute(""" 
                               SELECT *
                               FROM  Contract_TBL
                               WHERE Contract_TBL.RoomID = (?) AND Contract_TBL.Status = 'Active'
                               UNION
                               SELECT *
                               FROM  Booking_TBL
                               WHERE Booking_TBL.RoomID = (?) AND Booking_TBL.Status = 'Active'

                           """ ,(RoomID_Input,RoomID_Input,))

            result = cursor.fetchall()

            if result:
                check_booking_contract_active = True
            else:
                check_booking_contract_active = False          

            if not check_booking_contract_active :
                cursor.execute(""" INSERT INTO Booking_TBL (RoomID, 
                                                             CustomerID,
                                                             StartDate,
                                                             EndDate,
                                                             StaffID,
                                                             RoomFee,
                                                             InternetFee,
                                                             MaintenanceFee,
                                                             ParkingFee,
                                                             Remark,
                                                             Status) 
                                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                               """, (RoomID_Input, CustomerID_Input, StartDate_Input, EndDate_Input, EmployeeID_Input, RoomFee_Input,
                                     InternetFee_Input, MaintenanceFee_Input, ParkingFee_Input, Remark_Input, Status_Input))

                conn.commit()
                messagebox.showinfo("Success", "การจองเสร็จสมบูรณ์ กรุณาปริ้นท์เอกสารจองลงนาม")
                flag_fill_info_success = True
                return flag_fill_info_success

            else :
                messagebox.showinfo("Warning", "ห้องที่ต้องการติดจองหรือติดสัญญาอยู่ กรุณาเลือกห้องอื่น")
                flag_fill_info_success = False
                return flag_fill_info_success

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

        finally:
            if conn:
                conn.close()
    else :
        print("error")