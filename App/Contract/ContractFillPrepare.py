import sqlite3

from Config.Config import *
from tkinter import messagebox
from GetData.GetEmployeeID import get_employee_id

####################################################
# Get information from Database
####################################################
def prepare_contract_info(selected_room, first_name, last_name, register_date, register_end_date, employee, room_fee, internet, maintenance, parking, remark):
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
            print(name_parts[0])
            print(name_parts[1])

        EmployeeID_Input     = get_employee_id(name_parts[0],name_parts[1])

        RoomFee_Input        = room_fee  
        InternetFee_Input    = internet    
        MaintenanceFee_Input = maintenance
        ParkingFee_Input     = parking
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
def fill_contract_info(RoomID_Input, CustomerID_Input, StartDate_Input, EndDate_Input, EmployeeID_Input, RoomFee_Input, InternetFee_Input, MaintenanceFee_Input, ParkingFee_Input, Remark_Input, Status_Input):
    try:
        #print("Insert contract information to Database")

        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

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

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()
