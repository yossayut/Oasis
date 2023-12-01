import sqlite3

from Config.Config  import *
from tkinter        import messagebox

####################################################
# Get information from Database
####################################################
def get_employee_name_from_DB() :
    try:
        conn   = sqlite3.connect(Oasis_database_full_path)  
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT FirstName, LastName FROM Employee_TBL")
        employee_names = cursor.fetchall()

        if DEBUG == True :
             for item in employee_names:
                 print("get_employee_name => item : ",item)

        if not employee_names:
            return "ยังไม่มีพนักงาน"
        else:
            return employee_names

        return employee_names

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()