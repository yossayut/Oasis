import sqlite3

from Config.Config  import *
from tkinter        import messagebox

####################################################
# Get information from Database
####################################################
def get_customer_id_from_first_last_name(first_name,last_name) :
    try:
        conn   = sqlite3.connect(Oasis_database_full_path)
        cursor = conn.cursor()

        cursor.execute("SELECT CustomerID FROM Customer_TBL WHERE FirstName = ? AND LastName = ?", (first_name, last_name,))
        CustomerID_Input = cursor.fetchone()[0]
        
        return CustomerID_Input

        if DEBUG == True :
            if CustomerID_Input:
                print("get_customer_id => CustomerID_Input : ", CustomerID_Input)
            else:
                print("CustomerID_Input not found")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()