import sqlite3

from Config.Config  import *
from tkinter import messagebox

####################################################
# Get information from Database
####################################################
def get_employee_name() :
    try:
        conn = sqlite3.connect(Oasis_database_full_path)  
        cursor = conn.cursor()
        cursor.execute("SELECT FirstName, LastName FROM Employee_TBL")
        employee_names = cursor.fetchall()
        if DEBUG == True :
             for item in employee_names:
                 print(item)
        
        return employee_names

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()