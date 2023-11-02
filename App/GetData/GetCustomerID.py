import sqlite3

from Config.Config  import *
from tkinter import messagebox

####################################################
# Get information from Database
####################################################
def get_customer_id(first_name,last_name) :
    try:
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        cursor.execute("SELECT CustomerID FROM Customer_TBL WHERE FirstName = ? AND LastName = ?", (first_name, last_name,))
        CustomerID_Input = cursor.fetchone()[0]
        
        return CustomerID_Input

        if DEBUG == True :
            if CustomerID_Input:
                print("EmployeeID:", CustomerID_Input)
            else:
                print("Employee not found")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()