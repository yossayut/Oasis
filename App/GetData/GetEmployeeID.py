import sqlite3

from Config.Config  import *
from tkinter import messagebox

####################################################
# Get information from Database
####################################################
def get_employee_id(first_name,last_name) :
    try:
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        cursor.execute("SELECT EmployeeID FROM Employee_TBL WHERE FirstName = ? AND LastName = ?", (first_name, last_name,))
        EmployeeID_Input = cursor.fetchone()[0]
        
        return EmployeeID_Input

        if DEBUG == True :
            if EmployeeID_Input:
                print("EmployeeID:", EmployeeID_Input)
            else:
                print("Employee not found")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()